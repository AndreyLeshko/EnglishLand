# Generated by Django 4.0.4 on 2022-11-04 14:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('new_words', '0010_train_incorrect_ans_cnt_train_priority_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='train',
            options={'ordering': ('-last_try', 'word__english')},
        ),
        migrations.AddField(
            model_name='wordrussian',
            name='translates',
            field=models.ManyToManyField(through='new_words.Vocabulary', to='new_words.wordenglish'),
        ),
        migrations.AlterField(
            model_name='train',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trains', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='train',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trains', to='new_words.wordenglish', verbose_name='Слово'),
        ),
        migrations.AlterField(
            model_name='vocabulary',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='new_words.wordcategory', verbose_name='category'),
        ),
    ]
