from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Q, When, Case, Value

from new_words.models import Train, Vocabulary


# ======================================================================================================================
class CurrentTrain:

    def __init__(self, train_id):
        self.train_id = train_id
        self.http_status = 404
        self.is_owner = False
        self.train = self.get_train_obj()

    def get_train_obj(self):
        try:
            train_obj = Train.objects.get(pk=self.train_id)
            return train_obj
        except ObjectDoesNotExist:
            self.http_status = 404
            self.train = None

    def confirm_train_ownership(self, username):
        train_obj = self.get_train_obj()
        if username == train_obj.user.username:
            self.is_owner = True
        else:
            self.http_status = 403

    def inverse_train_status(self):
        if self.is_owner and self.train is not None:
            self.train.is_studied = not self.train.is_studied
            self.train.save()
            self.http_status = 201

    def increase_answer_counter(self, is_right):
        """
            - Увеличивает счетчик ответов на единницу
            - Обновляет счетчик прогресса
            - Обновляет значение приоритета
            - Сохраняет изменения
        """
        if self.is_owner and self.train is not None:
            if is_right:
                self.train.correct_ans_cnt += 1
            else:
                self.train.incorrect_ans_cnt += 1

            self._update_progress_counter(is_right)
            self._update_priority()

            self.train.save()
            self.http_status = 201

    def _update_progress_counter(self, is_right):
        if self.is_owner and self.train is not None:
            if is_right:
                self.train.progress += 4
                if self.train.progress > 100:
                    self.train.progress = 100
            else:
                self.train.progress -= 12
                if self.train.progress < 0:
                    self.train.progress = 0

    def _update_priority(self):
        """Пересчитывает значение приоритета"""
        progress = self.train.progress

        if 0 <= progress <= 20:
            new_priority = 5
        elif 21 <= progress <= 40:
            new_priority = 4
        elif 41 <= progress <= 60:
            new_priority = 3
        elif 61 <= progress <= 80:
            new_priority = 2
        else:
            new_priority = 1
        self.train.priority = new_priority


# ======================================================================================================================
class VocabularyObject:

    def __init__(self, en, ru):
        self.ru = ru
        self.en = en
        self.vocab_obj = self.find_vocabulary_object()

    def find_vocabulary_object(self):
        try:
            object = Vocabulary.objects.get(english__english=self.en, russian__russian=self.ru)
        except ObjectDoesNotExist:
            object = None
            print('NO', self.en)
        return object

    def get_possibility_translate_variants(self, number_of_variants):
        if self.vocab_obj:
            category = self.vocab_obj.category
            variants = {}
            # есть небольшая вероятность дублирования слов, так как distinct ищет уникальные пары en-ru
            variants_objects = Vocabulary.objects.filter(category=category) \
                                    .exclude(russian=self.vocab_obj.russian) \
                                    .exclude(english=self.vocab_obj.english) \
                                    .order_by('?') \
                                    .values(ru=F('russian__russian'), en=F('english__english')) \
                                    .distinct()[:number_of_variants]

            variants['ru'] = [variant['ru'] for variant in variants_objects]
            variants['en'] = [variant['en'] for variant in variants_objects]
            return variants
        else:
            return None
