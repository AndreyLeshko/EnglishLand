from django.contrib.auth.models import User
from django.db.models import Count

from new_words.models import Train


def get_user_words_statistic(user: User) -> dict:
    words_cnt = Train.objects.filter(user=user).values('status').annotate(count=Count('status')).order_by('status')
    context = {}
    if not words_cnt:
        context['on_study'] = 0
        context['studied'] = 0
    else:
        context['on_study'] = words_cnt[0]['count']
        context['studied'] = words_cnt[1]['count']
    return context
