from django import forms
from .models import *


class QuestionAdminForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['text', 'type', 'answer_options']

    def clean(self):

        cleaned_data = self.cleaned_data
        options = cleaned_data.get('answer_options')
        type = cleaned_data.get('type')

        if type != 'text' and options is None:
            raise forms.ValidationError('Please provide options in options field')

        return cleaned_data


class AnswerAdminForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['content', 'question']

    def clean(self):

        cleaned_data = self.cleaned_data
        content = cleaned_data.get('content')
        options = self.instance.question.answer_options
        type = self.instance.question.type

        print(type, options, content)

        if type == 'ChooseOneField':
            if content not in options.split(';'):
                raise forms.ValidationError(f'Select one field from {options}')
        elif type == "ChooseManyFields":
            if not all([ans in options.split(';') for ans in content.split(';')]):
                raise forms.ValidationError(f'Select many fields from {options}')

        return cleaned_data
