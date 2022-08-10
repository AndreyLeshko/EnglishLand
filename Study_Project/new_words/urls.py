from django.urls import path

from . import views


app_name = 'words'

urlpatterns = [
    path('api/words/', views.WordsAPIView.as_view()),
    path('en-ru-text/', views.words_en_ru_text, name='words_en_ru_text'),
    path('en-ru-text-result/', views.words_en_ru_text_result, name='words_en_ru_text_result'),
    path('echo-en-ru-text/', views.echo_words_en_ru_text, name='echo_words_en_ru_text'),
    path('echo-en-ru-text-result/', views.echo_words_en_ru_text_result, name='echo_words_en_ru_text_result'),
    path('train-words-1/', views.train_words_1, name='train_words_1'),
    path('train-words-1-result/', views.train_words_1_result, name='train_words_1_result'),
    path('add-words/', views.add_words_to_train, name='add_words_to_train'),
]