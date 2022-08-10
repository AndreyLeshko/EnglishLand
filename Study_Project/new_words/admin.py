from django.contrib import admin

from .models import Word, Train


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ['id', 'english', 'russian', 'category']



@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ['word', 'user', 'correct_ans_cnt', 'status']
