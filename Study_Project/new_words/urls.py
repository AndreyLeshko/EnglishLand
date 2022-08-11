from django.urls import path

from . import views


app_name = 'words'

urlpatterns = [
    path('api/words/', views.WordsAPIView.as_view()),
    path('words-text/<mode>/<how_translate>/', views.words_text, name='words_text'),
    path('words-text-result/<mode>/<how_translate>/', views.words_text_result, name='words_text_result'),
    path('add-words/', views.add_words_to_train, name='add_words_to_train'),
]