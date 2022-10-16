from django.core.exceptions import ObjectDoesNotExist

from new_words.models import Train


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
        """Увеличивает счетчик ответов на единницу и обновляет значение приоритета"""
        if self.is_owner and self.train is not None:
            if is_right:
                self.train.correct_ans_cnt += 1
            else:
                self.train.incorrect_ans_cnt += 1
            self.train.save()
            self._update_priority()
            self.http_status = 201

    def _update_priority(self):
        """Пересчитывает значение приоритета"""
        correct_ans_percent = self.train.correct_ans_cnt / \
                              (self.train.incorrect_ans_cnt + self.train.correct_ans_cnt) * 100
        if 0 <= correct_ans_percent <= 20:
            new_priority = 5
        elif 21 <= correct_ans_percent <= 40:
            new_priority = 4
        elif 41 <= correct_ans_percent <= 60:
            new_priority = 3
        elif 61 <= correct_ans_percent <= 80:
            new_priority = 2
        else:
            new_priority = 1
        self.train.priority = new_priority
        self.train.save()