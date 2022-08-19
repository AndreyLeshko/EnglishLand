from django.contrib import admin

from .models import Word, Train


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ['id', 'english', 'russian', 'category']
    search_fields = ['english', 'russian']



@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ['pk', 'word', 'user', 'correct_ans_cnt', 'status']
    search_fields = ['user']
