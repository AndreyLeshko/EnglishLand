from django.urls import path

from . import views


app_name = 'words'

urlpatterns = [
    # API
    path('api/words/', views.WordsAPIView.as_view()),
    path('api/words/word/train/', views.WordTrainAPIView.as_view()),

    # Trainer
    path('words-text/<mode>/<how_translate>/', views.words_text, name='words_text'),
    path('words-text-result/<mode>/<how_translate>/', views.words_text_result, name='words_text_result'),
    path('words-with-variants/<mode>/<how_translate>/', views.words_with_variants, name='words_with_variants'),

    # DB
    path('add-new-word/', views.add_word, name='add_word'),

    # Trains management
    path('trains/add-words-to-train/', views.add_words_to_train, name='add_words_to_train'),
    path('trains/change-status/<int:train_id>/', views.change_train_status, name='change_train_status'),
    # path('trains/increase-attempt-counter/<int:train_id>', views.increase_attempt_counter, name='increase_attempt_counter')
]