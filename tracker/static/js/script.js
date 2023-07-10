function save_frequency() {
    const BtnSaveFrequency = document.querySelector('.btn_save_frequency');
    const RadioFrequency = document.querySelectorAll('.frequency_radio');
    const InputFrequency = document.querySelectorAll('.data_input_frequency');
    const FormFrequency = document.querySelector('.form_frequency');

    let active_radio = '';


    RadioFrequency.forEach((radio) => {
        if (radio.checked) {
            active_radio = radio.value;
        };
        });

    let status = ''

    if (active_radio == 'fr_1') {
        status = 'Каждый день'
        }

    else if (active_radio == 'fr_2') {
        status = `Каждые ${document.querySelector('#frv_2').value} дней`
        }

    else if (active_radio == 'fr_3') {
        status = `${document.querySelector('#frv_3').value} раз в неделю`
        }

    else if(active_radio == 'fr_4') {
        status = `${document.querySelector('#frv_4').value} раз в месяц`
        }

    InputFrequency.forEach((item) => {
        item.value = status;
    });

    FormFrequency.close();
    };


function edit_hm(id) {
    const EditHmForm = document.querySelector('.edit_hm_action_form');
    document.querySelector('#HM_habit_id').value = id;
    EditHmForm.show();
    };


function show_form_el(habit) {
    const elInfoForm = document.querySelector('.el_info_form');
    elInfoForm.style.display = 'block';

    document.querySelector("#el_info_form_span").textContent = habit.title;
    document.querySelector("#habit_id_el_info").value = habit.habit_id;
    document.querySelector("#el_info_data_frequency").textContent = habit.frequency;
    document.querySelector("#el_info_data_frequency").style.color = habit.color;


    let calendar = document.querySelectorAll(".el_info_calendar_btn_data")

    calendar.forEach((date) => {
        if (habit.type_habit == 'HM') {
            if (Number(habit.actions[date.value]) >= Number(habit.target)) {
                document.querySelector(`#calendar_btn_${date.name}`).style.background = habit.color;
            }

            else if (Number(habit.actions[date.value]) > 0) {
                document.querySelector(`#calendar_btn_${date.name}`).style.background = habit.color;
                document.querySelector(`#calendar_btn_${date.name}`).style.opacity = `.${parseInt(100 / Number(habit.target) * Number(habit.actions[date.value]), 10) - 10}`;
            }

            else {
                document.querySelector(`#calendar_btn_${date.name}`).style.background = '#424242';
                document.querySelector(`#calendar_btn_${date.name}`).style.opacity = "1";
            }}
        else {
            if (Number(habit.actions[date.value]) == 1) {
            document.querySelector(`#calendar_btn_${date.name}`).style.background = habit.color;
            }
            else {
                document.querySelector(`#calendar_btn_${date.name}`).style.background = '#424242';
                document.querySelector(`#calendar_btn_${date.name}`).style.opacity = "1";
            }
        }});

    document.querySelectorAll('.el_info_data_title').forEach((item) => {
        item.style.color = habit.color;
    });

    document.querySelector('#el_info_data_all').textContent = `Всего дней: ${habit.all_action}`
    document.querySelector('#el_info_data_best').textContent = `Лучшая серия: ${habit.best_actions}`
    document.querySelector('#el_info_data_current').textContent = `На данный момент: ${habit.counter}`


    if (Number(`${habit.counter}`) >= 21) {
        document.querySelector('.habit_done').hidden = false
    };

    document.querySelectorAll(".bt_edit").forEach((btn) => {
        btn.addEventListener('click', () => {
            elInfoForm.style.display = 'none';

            if (habit.type_habit == 'YN') {
                document.querySelector('#type_form_habit_yn').value = 'edit';
                document.querySelector('#addHabit_text_yn').textContent = 'Изменить привычку';
                document.querySelector('#YN_data_input_title').value = habit.title;
                document.querySelector('#YN_data_input_color').value = habit.color;
                document.querySelector('#YN_btn_color').style.background = habit.color;
                document.querySelector('#YN_data_input_question').value = habit.question;
                document.querySelector('#YN_data_input_frequency').value = habit.frequency;
                document.querySelector('#habit_id_yn').value = habit.habit_id;

                document.querySelector('#addHabitYN').show();
            }

            else if (habit.type_habit == 'HM') {
                document.querySelector('#type_form_habit_hm').value = 'edit';
                document.querySelector('#addHabit_text_hm').textContent = 'Изменить привычку';

                document.querySelector('#HM_data_input_title').value = habit.title;
                document.querySelector('#HM_data_input_color').value = habit.color;
                document.querySelector('#HM_btn_color').style.background = habit.color;

                document.querySelector('#HM_data_input_question').value = habit.question;
                document.querySelector('#HM_data_input_frequency').value = habit.frequency;
                document.querySelector('#HM_data_input_units').value = habit.units;
                document.querySelector('#HM_data_input_target').value = habit.target;
                document.querySelector('#habit_id_hm').value = habit.habit_id;
                document.querySelector('#addHabitHM').show();
            }
      })})

    return
};


function archive() {
    document.getElementById("MainDropdown").classList.remove('show');
    document.querySelector('.archive_form').show();


};


function edit_habit() {
    alert(document.querySelector('#el_info_form_span').textContent);
};


function close_form() {
    const elInfoForm = document.querySelector('.el_info_form');
    elInfoForm.style.display = 'none';
    const addForms = document.querySelectorAll('.addHabitForm')

    addForms.forEach((form) => {
        form.close();
        });
//    elInfoForm.close();
};


function close_delete_form() {
    document.querySelector('.delete_form').close()
};

function close_habit_done_form() {
    document.querySelector('.habit_done_form').close()
};

function close_archive_form() {
    document.querySelector('.archive_form').close();
};

function btn_burger() {
    document.getElementById("MainDropdown").classList.toggle("show");

    window.onclick = function(event) {
        if (event.target.classList != '' && event.target.classList != 'dropdown') {
            document.getElementById("MainDropdown").classList.remove('show');
            return
        }
    }
};


function el_info_bt_dop() {
    document.getElementById("myDropdown").classList.toggle("show");

    window.onclick = function(event) {
        if (event.target.classList != '' && event.target.classList != 'dropdown') {
            document.getElementById("myDropdown").classList.remove('show');
            return
        }
    }
};


function delete_el_form() {
    document.getElementById("myDropdown").classList.remove('show');
    document.querySelector('.delete_form').show();
    document.querySelector('#delete_habit').value = document.querySelector('#habit_id_el_info').value
};


function habit_done () {
    document.querySelector('.habit_done_form').show();
    document.querySelector('#habit_done').value = document.querySelector('#habit_id_el_info').value
}

