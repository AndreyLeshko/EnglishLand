from django.test import TestCase

from new_words.models import WordEnglish


class WordEnglishTestCase(TestCase):

    def setUp(self):
        WordEnglish.objects.create(english='window')

    def test_word_representation(self):
        word = WordEnglish.objects.get(english='window')
        self.assertEqual(str(word), 'window')