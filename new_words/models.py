from django.contrib.auth.models import User
from django.db import models


class Word(models.Model):
    categories = [
        ('NOUN', 'noun'),
        ('VERB', 'verb'),
        ('ADJECTIVE', 'adjective'),
        ('ADVERB', 'adverb'),
        ('PARTICIPLE', 'participle'),
        ('PRONOUN', 'pronoun'),
        ('OTHER', 'other'),
        ('UNKNOWN', 'unknown'),
    ]

    english = models.CharField(max_length=100)
    russian = models.CharField(max_length=100)
    category = models.CharField(max_length=15, choices=categories, default='UNKNOWN')

    def __str__(self):
        return f"({self.id}) {self.english}"


class Train(models.Model):

    status_list = [('studied', 'studied'), ('on study', 'on study')]

    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    correct_ans_cnt = models.IntegerField(default=0)
    status = models.CharField(max_length=15, choices=status_list, default='on study')
    last_try = models.DateField(auto_now=True)
