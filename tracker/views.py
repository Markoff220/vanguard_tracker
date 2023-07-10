from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from datetime import datetime, timedelta
from django.shortcuts import redirect

from tracker.models import User, Habit, Action, Archive


def get_correct_day_word(frequency):
    if 'Каждые' in frequency:
        number = str([i for i in str(frequency.split(' ')[1])][-1])
        data = frequency.split(' ')[:2]

        if number == '1':
            data.append('день')

        elif number in ('2', '3', '4'):
            data.append('дня')

        else:
            data.append('дней')

        return ' '.join(data)

    return frequency


def get_date_habit(day=1, date_format='%d.%m.%Y'):
    day = int(day) - 1
    today = datetime.now()
    data = today - timedelta(days=day)

    return str(data.strftime(date_format))


def get_missed_action(date, date_format='%d.%m.%Y'):
    data = datetime.strptime(date, date_format) + timedelta(days=1)

    return str(data.strftime(date_format))


def get_counter(actions, target, frequency):
    counter = 0

    if frequency == 'Каждый день':
        for index_action, action in enumerate(actions):
            if index_action == 0 and not action.status:
                pass

            elif action.status and int(action.status) >= int(target):
                counter += 1

            else:
                return counter

        return counter

    elif 'каждые' in frequency.lower():
        space = int(frequency.split(' ')[1])
        temp = 0

        for index_action, action in enumerate(actions):
            if index_action == 0 and not action.status:
                pass

            elif action.status and int(action.status) >= int(target):
                counter += 1
                temp = 0

            else:
                temp += 1

                if temp == space:
                    return counter
        return counter

    else:
        n = 0
        if 'месяц' in frequency.lower():
            n = 30

        elif 'неделю' in frequency.lower():
            n = 7

        space = int(frequency.split(' ')[0])

        chunks = [actions[i:i + n] for i in range(0, len(actions), n)]

        for count_chunk, chunk in enumerate(chunks):
            if target == 0:
                successful_days = list(map(lambda action: int(action.status) > int(target), chunk)).count(True)
            else:
                successful_days = list(map(lambda action: int(action.status) >= int(target), chunk)).count(True)

            if count_chunk == 0:
                counter += successful_days

            else:
                if successful_days >= space:
                    counter += successful_days

        return counter


def get_best_counter(actions, target, frequency):
    best = 0
    counter = 0
    counter_lose = 0

    if frequency == 'Каждый день':
        for index_action, action in enumerate(actions):
            if index_action == 0 and not action.status:
                pass

            elif action.status and int(action.status) >= int(target):
                counter += 1

            else:
                if counter > best:
                    best = counter

                counter = 0

        if counter > best:
            best = counter

        return best

    elif 'каждые' in frequency.lower():
        space = int(frequency.split(' ')[1])

        for index_action, action in enumerate(actions):
            if index_action == 0 and not action.status:
                pass

            elif action.status and int(action.status) >= int(target):
                counter += 1

            else:
                counter_lose += 1
                if counter_lose == space:
                    if counter > best:
                        best = counter

                        counter_lose = 0
                        counter = 0
        if counter > best:
            best = counter

        return best

    else:
        space = int(frequency.split(' ')[0])
        n = 0

        if 'месяц' in frequency.lower():
            n = 30

        elif 'неделю' in frequency.lower():
            n = 7

        chunks = [actions[i:i + n] for i in range(0, len(actions), n)]

        for count_chunk, chunk in enumerate(chunks):
            if target == 0:
                successful_days = list(map(lambda action: int(action.status) > int(target), chunk)).count(True)
            else:
                successful_days = list(map(lambda action: int(action.status) >= int(target), chunk)).count(True)

            if count_chunk == 0:
                counter += successful_days

            else:
                if successful_days >= space:
                    counter += successful_days

                else:
                    if counter > best:
                        best = counter
                        counter = 0
        if counter > best:
            best = counter

        return best


def tracker_main(request):
    telegram_id = request.GET.get('user')
    user_obj = User.objects.filter(telegram_id=telegram_id)

    if len(user_obj):
        user = user_obj[0]

    else:
        user = User(telegram_id=request.GET.get('user'), username='username')
        user.save()

    user_habits = Habit.objects.filter(user=user)

    HABITS = []

    for habit in user_habits:
        while True:
            actions = Action.objects.filter(habit=habit)
            last_date = actions[len(actions) - 1].date

            if last_date != get_date_habit():
                new_action = {
                    'habit': habit,
                    'date': get_missed_action(last_date),
                    'status': 0
                }
                action = Action(**new_action)
                action.save()

            else:
                break

        actions = [action for action in reversed(actions)]
        actions_data = {}
        calendar = {}

        for action in actions[:5]:
            actions_data[action.date] = int(action.status)

        for date in [get_date_habit(i, '%d.%m.%Y') for i in range(1, 130)]:
            action = Action.objects.filter(date=date, habit=habit)
            if action:
                calendar[date] = action[0].status
            else:
                calendar[date] = 0

        HABITS.append({
            'habit_id': habit.id,
            'title': habit.title,
            'type_habit': habit.type_habit,
            'color': habit.color,
            'question': habit.question,
            'actions': actions_data,
            'target': habit.target,
            'frequency': habit.frequency,
            'units': habit.units,
            'counter': get_counter(actions, habit.target, habit.frequency),
            'all_action': len(actions) - 4,
            'best_actions': get_best_counter(actions, habit.target, habit.frequency),
            'calendar': calendar
        })

    calendar = []
    temp = []
    for i in range(1, 130):
        if get_date_habit(i, '%a') == 'Mon':
            temp.append(get_date_habit(i, '%d.%m.%Y'))
            calendar.append(reversed(temp))
            temp = []

        else:
            temp.append(get_date_habit(i, '%d.%m.%Y'))

    calendar.append(reversed(temp))
    context = {
        'habits': HABITS,
        'dates': [get_date_habit(i, '%d %a') for i in range(1, 6)],
        'calendar': calendar,
        'archive_habits': Archive.objects.all()
    }

    # Обработчик событий
    if request.POST:
        # Обновление статуса привычки
        if request.POST.get('change_habit_status'):
            habit_action = request.POST.get('change_habit_status')

            change_habit = user_habits.filter(id=habit_action.split('_')[0])[0]
            change_action = Action.objects.filter(habit=change_habit,
                                                  date=get_date_habit(habit_action.split('_')[1]))[0]
            if change_habit.type_habit == 'YN':
                change_action.status = '0' if int(change_action.status) else '1'
                change_action.save()

            elif change_habit.type_habit == 'HM':
                if str(request.POST.get('HM_value')).isdigit():
                    change_action.status = request.POST.get('HM_value')
                    change_action.save()

        # Создание новой привычки и редактирование существующей
        elif request.POST.get('color'):
            data_habit = {
                'title': request.POST.get('title'),
                'type_habit': request.POST.get('type_habit'),
                'question': request.POST.get('question', ''),
                'color': request.POST.get('color'),
                'frequency': get_correct_day_word(request.POST.get('frequency')),
                'units': request.POST.get('units', ''),
                'target': request.POST.get('target', 0)
            }

            # Новая
            if request.POST.get('type_form_habit') == 'new':
                data_habit['user'] = user
                new_habit = Habit(**data_habit)
                new_habit.save()

                for i in range(5, 0, -1):
                    action = Action(habit=new_habit,
                                    date=get_date_habit(i),
                                    status=0)

                    action.save()

            # Редактирование
            elif request.POST.get('type_form_habit') == 'edit':
                habit = Habit.objects.filter(user=user, id=request.POST.get('habit_id'))
                habit.update(**data_habit)

        # Удаление привычки
        elif request.POST.get('delete_habit'):
            habit_id = int(request.POST.get('delete_habit'))
            obj = Habit.objects.filter(id=habit_id)
            obj.delete()

        # Завершение привычки
        elif request.POST.get('habit_done'):
            habit_id = int(request.POST.get('habit_done'))

            habit = Habit.objects.filter(id=habit_id)[0]

            data = {
                'user': habit.user,
                'title': habit.title,
                'type_habit': habit.type_habit,
                'question': habit.question,
                'color': habit.color,
                'frequency': habit.frequency,
                'units': habit.units,
                'target': habit.target,
                'date_start': get_date_habit(day=len(Action.objects.filter(habit=habit)) - 4),
                'date_finish': get_date_habit()
            }
            done_habit = Archive(**data)
            done_habit.save()

            habit.delete()

        return HttpResponsePermanentRedirect(f"/tracker/?user={telegram_id}")

    elif request.GET:
        return render(request, 'index.html', context)


def create_new_user(request):
    user = User(telegram_id='404820105', username='Cas220')
    user.save()
    return HttpResponse('Создан новый пользователь. <a href="/tracker">Трекер</a>')