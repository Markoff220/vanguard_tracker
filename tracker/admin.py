from django.contrib import admin
from .models import User, Habit, Action, Archive

# Register your models here.


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'username']


@admin.register(Habit)
class UserHabitsAdmin(admin.ModelAdmin):
    pass


@admin.register(Action)
class UserActionsAdmin(admin.ModelAdmin):
    pass


@admin.register(Archive)
class UserArchiveAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'date_start', 'date_finish']