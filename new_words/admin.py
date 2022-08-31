from django.contrib import admin

from .models import WordEnglish, WordRussian, WordCategory, Vocabulary, Train


@admin.register(WordEnglish)
class WordEnglishAdmin(admin.ModelAdmin):
    list_display = ['pk', 'english']
    search_fields = ['english']


@admin.register(WordRussian)
class WordRussianAdmin(admin.ModelAdmin):
    list_display = ['pk', 'russian']
    search_fields = ['russian']


@admin.register(WordCategory)
class WordCategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name']


@admin.register(Vocabulary)
class VocabularyAdmin(admin.ModelAdmin):
    list_display = ['english', 'russian', 'category']


@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ['pk', 'word', 'user', 'correct_ans_cnt', 'is_studied']
    search_fields = ['user']
