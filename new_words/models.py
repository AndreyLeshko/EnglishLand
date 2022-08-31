from django.contrib.auth.models import User
from django.db import models


class WordEnglish(models.Model):
    english = models.CharField(max_length=100, unique=True)
    translates = models.ManyToManyField('WordRussian', through='Vocabulary')

    def __str__(self):
        return f'{self.english}'


class WordRussian(models.Model):
    russian = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.russian}'


class WordCategory(models.Model):
    category_name = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.category_name}'


class Vocabulary(models.Model):
    english = models.ForeignKey(WordEnglish, related_name='vocabulary', verbose_name='english_word_tb',
                                on_delete=models.CASCADE)
    russian = models.ForeignKey(WordRussian, related_name='vocabulary', verbose_name='russian_word_tb',
                                on_delete=models.CASCADE)
    category = models.ForeignKey(WordCategory, null=True, on_delete=models.SET_NULL)


class Train(models.Model):
    word = models.ForeignKey(WordEnglish, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    correct_ans_cnt = models.IntegerField(default=0)
    is_studied = models.BooleanField(default=False)
    last_try = models.DateField(auto_now=True)
