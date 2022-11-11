from django.urls import path
from django.views.generic import TemplateView

from . import views


app_name = 'words'

urlpatterns = [
    # API
    path('api/words/', views.WordsAPIView.as_view()),
    path('api/train-object/', views.TrainObjectAPIView.as_view()),
    path('api/get-variants/<int:number_variants>/', views.get_possible_variants),
    path('api/words/', views.WordsAPIView.as_view(), name='words'),
    path('api/words/<int:pk>/', views.WordDetailApiView.as_view(), name='words_detail'),
    path('api/add-word-to-train/', views.AddWordToTrain.as_view(), name='add_word_to_train'),

    # Trainer
    path('words-text/', views.words_text, name='words_text'),
    path('words-with-variants/', views.words_with_variants, name='words_with_variants'),

    # DB
    path('add-new-word/', views.add_word, name='add_word'),
    path('words-review/', views.WordsReviewView.as_view(), name='words_review'),

    # Trains management
    path('trains/add-words-to-train/', views.add_words_to_train, name='add_words_to_train'),
    path('trains/change-status/<int:train_id>/', views.change_train_status, name='change_train_status'),
    path('trains/increase-attempt-counter/<int:train_id>/<is_right>/', views.increase_attempt_counter, name='increase_attempt_counter')
]