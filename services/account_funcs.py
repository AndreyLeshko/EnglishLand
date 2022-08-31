from django.contrib.auth.models import User
from django.db.models import Count

from new_words.models import Train


def get_user_words_statistic(user: User) -> dict:
    words_cnt = Train.objects.filter(user=user).values('is_studied').annotate(count=Count('is_studied'))
    context = {'on_study': 0, 'studied': 0}
    for status in words_cnt:
        if status['is_studied']:
            context['studied'] = status['count']
        elif not status['is_studied']:
            context['on_study'] = status['count']
    return context
