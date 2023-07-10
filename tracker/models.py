from django.db import models
from django import forms


class User(models.Model):
    telegram_id = models.CharField(max_length=20)
    username = models.CharField(max_length=20)


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    type_habit = models.CharField(max_length=10)
    question = models.CharField(max_length=50)
    color = models.CharField(max_length=10)
    frequency = models.CharField(max_length=20)

    units = models.CharField(max_length=10)
    target = models.IntegerField()


class Action(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.CharField(max_length=10)
    status = models.IntegerField()


class Archive(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    type_habit = models.CharField(max_length=10)
    question = models.CharField(max_length=50)
    color = models.CharField(max_length=10)
    frequency = models.CharField(max_length=20)

    units = models.CharField(max_length=10)
    target = models.IntegerField()

    date_start = models.CharField(max_length=15)
    date_finish = models.CharField(max_length=15)