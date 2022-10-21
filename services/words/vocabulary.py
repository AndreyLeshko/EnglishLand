from django.db.models import F

from new_words.models import Vocabulary


class EnWordTranslates:

    def __init__(self, word_en):
        self.word_en = word_en
        self.translates = self.get_translates()

    def get_translates(self):
        translates = [word['translate'] for word in Vocabulary.objects
                                                            .filter(english__english=self.word_en)
                                                            .values(translate=F('russian__russian'))]
        return translates

    def __str__(self):
        return f"{self.word_en}: {self.translates}"


class RuWordTranslates:

    def __init__(self, word_ru):
        self.word_ru = word_ru
        self.translates = self.get_translates()

    def get_translates(self):
        translates = [word['translate'] for word in Vocabulary.objects
                                                            .filter(russian__russian=self.word_ru)
                                                            .values(translate=F('english__english'))]
        return translates

    def __str__(self):
        return f"{self.word_ru}: {self.translates}"