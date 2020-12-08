from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Survey(models.Model):
    name = models.CharField(max_length=100, blank=False)
    date_start = models.DateTimeField(default=now, editable=False)
    date_end = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=2000, default="")

    def __str__(self):
        return self.name


class Question(models.Model):
    type_choices = (
        ('ChooseOneField', 'ChooseOneField'),
        ('ChooseManyFields', 'ChooseManyFields'),
        ('text', 'Text')
    )
    text = models.CharField(max_length=500)
    type = models.CharField(max_length=16, choices=type_choices, default='text')
    answer_options = models.CharField(max_length=1000, null=True, blank=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)

    class Meta:
        unique_together = ['user', 'question']

