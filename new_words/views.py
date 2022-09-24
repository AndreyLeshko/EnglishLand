from random import shuffle

from django.shortcuts import render
from rest_framework import generics
from django.http.response import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .serializers import WordSerializer
from services import new_words_funcs


# ======================================================================================================================
# API

class WordsAPIView(generics.ListAPIView):
    # queryset = WordEnglish.objects.all()
    serializer_class = WordSerializer


# ======================================================================================================================
# перевод текстом en->ru / ru->en
# mode = ['all_words', 'user_words', 'repeat_words']
# how_translate = ['en-ru', 'ru-en']

@login_required
def words_text(request, mode, how_translate):
    """Выбирает слово из нужной категории (все слова / на изучении / изученные), на заданном языке"""

    if how_translate == 'ru-en':
        source_lang = 'russian'
        translate_lang = 'english'
    else:
        source_lang = 'english'
        translate_lang = 'russian'

    context = {}

    if mode == 'all_words':
        word_obj = new_words_funcs.get_random_word()
        if not word_obj:
            context['empty'] = 1
        else:
            context['word'] = getattr(word_obj, f'{source_lang}_word_tb.{source_lang}')
            context['translate'] = getattr(word_obj, f'{translate_lang}_word_tb.{translate_lang}')
            context['train_id'] = ''

    elif mode == 'user_words':
        cur_train_obj = new_words_funcs.get_train_word_object(request, is_studied=False)
        if not cur_train_obj:
            context['empty'] = 1
        else:
            if how_translate == 'ru-en':
                context['word'] = cur_train_obj.word.translates.first()
            else:
                context['word'] = cur_train_obj.word.english
            context['train_id'] = cur_train_obj.pk

    elif mode == 'repeat_words':
        cur_train_obj = new_words_funcs.get_train_word_object(request, is_studied=True)
        if not cur_train_obj:
            context['empty'] = 1
        else:
            if how_translate == 'ru-en':
                context['word'] = cur_train_obj.word.translates.first()
            else:
                context['word'] = cur_train_obj.word.english
            context['train_id'] = cur_train_obj.pk

    context['mode'] = mode
    context['how_translate'] = how_translate

    return render(request, 'new_words/words_text.html', context=context)


@login_required
def words_text_result(request, mode, how_translate):
    """
    Проверяет правильность введенного перевода, выбирает другие возможные переводы, меняет статус (изучено/на изучении)
    """
    word = request.POST['word']
    train_id = request.POST['train_id']
    translate_attempt = request.POST['translate_attempt'].strip().lower()

    translates = new_words_funcs.get_possible_translations(word, how_translate)

    is_correct = False  # правильно ли перевёл пользователь
    other_translates_list = []  # список других переводов слова
    context = {}

    for translate in translates:
        if translate == translate_attempt:
            is_correct = True
        else:
            other_translates_list.append(translate)

    new_words_funcs.increase_answer_counter(train_id, is_correct)

    if not is_correct:
        context['translate'] = other_translates_list.pop(0)

    if request.POST.get('need_train'):
        if mode == 'all_words':
            new_words_funcs.add_word_to_train(request.user, how_translate, word)
        elif mode == 'user_words':
            new_words_funcs.change_status_is_studied(train_id, new_status=True)
        elif mode == 'repeat_words':
            new_words_funcs.change_status_is_studied(train_id, new_status=False)

    context['word'] = word
    context['is_correct'] = is_correct
    context['other_translates'] = other_translates_list
    context['translate_attempt'] = translate_attempt
    context['mode'] = mode
    context['how_translate'] = how_translate

    return render(request, 'new_words/words_text_result.html', context=context)


# ======================================================================================================================
# перевод с вариантами en->ru / ru->en
# mode = ['user_words']
# how_translate = ['en-ru', 'ru-en']

@login_required
def words_with_variants(request, mode, how_translate):

    context = {}

    if mode != 'user_words':
        return HttpResponseNotFound(f'No such mode as {mode}')

    cur_train_obj = new_words_funcs.get_train_word_object(request, is_studied=False)

    if not cur_train_obj:
        context['empty'] = 1
    else:
        if how_translate == 'ru-en':
            context['word'] = cur_train_obj.word.translates.order_by('?').first()
            context['translate'] = cur_train_obj.word.english
        else:
            context['word'] = cur_train_obj.word.english
            context['translate'] = cur_train_obj.word.translates.order_by('?').first()

        cur_train_obj.save()  # обновлляет дату последней попытки модели Train

        variants_list = new_words_funcs.get_wrong_translation_variants(cur_train_obj, how_translate)

        variants_list.append(context['translate'])
        shuffle(variants_list)
        context['variants'] = variants_list

    context['mode'] = mode
    context['how_translate'] = how_translate

    return render(request, 'new_words/words_with_variants.html', context=context)


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
