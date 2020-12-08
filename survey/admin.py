from django.contrib import admin
from .models import *
from .forms import *


class QuestionTabular(admin.TabularInline):
    form = QuestionAdminForm
    model = Question


@admin.register(Survey)
class SurveySystemAdmin(admin.ModelAdmin):
    readonly_fields = ('date_start',)
    inlines = [QuestionTabular, ]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    form = AnswerAdminForm
