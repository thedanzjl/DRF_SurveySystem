# Generated by Django 2.2.10 on 2020-12-07 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_auto_20201207_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.CharField(choices=[('ChooseOneField', 'ChooseOneField'), ('ChooseManyFields', 'ChooseManyFields'), ('text', 'Text')], default='text', max_length=16),
        ),
    ]
