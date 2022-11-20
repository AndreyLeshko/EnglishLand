# Generated by Django 4.0.4 on 2022-11-18 09:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new_words', '0011_alter_train_options_wordrussian_translates_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wordenglish',
            options={'ordering': ('english',)},
        ),
        migrations.AddField(
            model_name='train',
            name='progress',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(40)], verbose_name='Счетчик прогресса'),
        ),
    ]