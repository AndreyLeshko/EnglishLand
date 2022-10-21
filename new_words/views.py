from random import shuffle

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http.response import HttpResponseNotFound, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from .models import WordEnglish
from .serializers import WordSerializer, WordTrainSerializer, TrainObjectSerializer
from services import new_words_funcs
from services.words import trains, vocabulary


# ======================================================================================================================
# API

class WordsAPIView(generics.ListAPIView):
    queryset = WordEnglish.objects.all()
    serializer_class = WordSerializer


class TrainObjectAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.GET['mode'] == 'study':
            train_obj = new_words_funcs.get_train_word_object(request, is_studied=False)
        elif request.GET['mode'] == 'repeat':
            train_obj = new_words_funcs.get_train_word_object(request, is_studied=True)
        serializer = TrainObjectSerializer(train_obj)
        context = serializer.data
        context['word'] = new_words_funcs.translates_dict(train_obj)
        return Response({'train': context})


# ======================================================================================================================
# Тренировки

@login_required
def words_text(request):
    return render(request, 'new_words/words_text.html')


@login_required
def words_with_variants(request):
    return render(request, 'new_words/words_with_variants.html')


# ======================================================================================================================
# добавление/смена статуса слов

@login_required
def add_words_to_train(request):
    """Показывает список неизученных слов, отмеченные слова добавляет для тренировки"""

    if request.method == 'POST':
        for param in request.POST:
            if 'on' in request.POST[param]:
                new_words_funcs.add_word_to_train(request.user, how_translate='en-ru', word=param)

    new_words = new_words_funcs.get_new_words_for_user(request.user)
    paginator = Paginator(new_words, 20)
    page = request.GET.get('page')
    try:
        words = paginator.page(page)
    except PageNotAnInteger:
        words = paginator.page(1)
    except EmptyPage:
        words = paginator.page(paginator.num_pages)
    return render(request, 'new_words/add_words_to_train.html', context={'words': words, 'page': page})


# ======================================================================================================================
# добавление слов

@login_required
def add_word(request):
    context = dict()
    context['categories'] = new_words_funcs.get_category_list()
    if request.method == 'POST':
        en = request.POST['english'].strip()
        ru = request.POST['russian'].strip()
        category = request.POST['category']
        new_words_funcs.add_new_word_to_db(en, ru, category)
        context['added_word'] = request.POST['english'].strip()
    return render(request, 'new_words/add_word.html', context=context)


# ======================================================================================================================
# Управление тренировками

def change_train_status(request, train_id):
    """
        Инвертирует статус тренировки
        Коды ответов:
            201 - успешно
            403 - блокировка доступа
            404 - неверные данные
    """
    cur_train = trains.CurrentTrain(train_id)
    cur_train.confirm_train_ownership(request.user.username)
    cur_train.inverse_train_status()
    return HttpResponse(status=cur_train.http_status)


def increase_attempt_counter(request, train_id, is_right):
    """
        Увеличивает счетчик ответов (правильных или неправильных)
        для правильных ответов is_right передаётся как 'true', для неправильных 'false'
        Коды ответов:
            201 - успешно
            403 - блокировка доступа
            404 - неверные данные
    """
    is_right = True if is_right == 'true' else False
    cur_train = trains.CurrentTrain(train_id)
    cur_train.confirm_train_ownership(request.user.username)
    cur_train.increase_answer_counter(is_right)
    return HttpResponse(status=cur_train.http_status)


def get_possible_variants(request, number_variants):
    en = request.GET['en']
    ru = request.GET['ru']
    source = trains.VocabularyObject(en, ru)
    return JsonResponse({
        'variants': source.get_possibility_translate_variants(number_variants)
    })

# ======================================================================================================================
#
