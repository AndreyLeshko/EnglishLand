# Generated by Django 4.0.4 on 2022-08-29 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('new_words', '0007_vocabulary_wordcategory_wordrussian_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vocabulary',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='new_words.wordcategory'),
        ),
    ]
