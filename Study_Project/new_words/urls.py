from django.urls import path

from . import views


app_name = 'words'

urlpatterns = [
    path('api/words/', views.WordsAPIView.as_view()),
    path('user-words-train', views.user_words_train, name='user_words_train'),
    path('user-words-train-result', views.user_words_train_result, name='user_words_train_result'),
    path('train-words-1/', views.train_words_1, name='train_words_1'),
    path('train-words-1-result/', views.train_words_1_result, name='train_words_1_result'),
    path('add-words/', views.add_words_to_train, name='add_words_to_train'),
]