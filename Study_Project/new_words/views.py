from django.shortcuts import render
from rest_framework import generics
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import Word, Train
from .serializers import WordSerializer


class WordsAPIView(generics.ListAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer


# ======================================================================================================================
# en -> ru (только слова пользователя), перевод текстом

@login_required
def words_en_ru_text(request):
    cur_train = Train.objects.filter(user=request.user).filter(status='on study').select_related('word').order_by('?').first()
    return render(request, 'new_words/words_en_ru_text.html', context={'cur_train': cur_train})


@login_required
def words_en_ru_text_result(request):
    word_en = request.POST['word-en']
    translate_attempt = request.POST['translate'].strip().lower()
    right_translate = request.POST['word-ru']
    train_id = request.POST['train_id']

    translates = Word.objects.filter(english=word_en).values('russian')
    is_correct = False
    other_translates_list = []
    for i in translates:
        if i['russian'] == translate_attempt:
            is_correct = True
            cur_train = Train.objects.get(pk=train_id)
            cur_train.correct_ans_cnt += 1
            cur_train.save()
        other_translates_list.append(i['russian'])

    if translate_attempt in other_translates_list:
        other_translates_list.remove(translate_attempt)
    if right_translate in other_translates_list:
        other_translates_list.remove(right_translate)

    if 'on' in request.POST['stud']:
        cur_train = Train.objects.get(pk=train_id)
        cur_train.status = 'studied'
        cur_train.save()

    context = {
        'word_en': word_en,
        'translate_attempt': translate_attempt,
        'right': right_translate,
        'is_correct': is_correct,
        'other_translates': other_translates_list,
    }
    return render(request, 'new_words/words_en_ru_text_result.html', context=context)


# ======================================================================================================================
# перевод текстом (слова пользователя) en->ru / ru->en

# mode = ['all_words', 'user_words', 'repeat_words']
# how_translate = ['en-ru', 'ru-en']

@login_required
def words_text(request, mode, how_translate):
    if how_translate == 'ru-en':
        source_lang = 'russian'
        translate_lang = 'english'
    else:
        source_lang = 'english'
        translate_lang = 'russian'

    context = {}

    if mode == 'all_words':
        word_obj = Word.objects.order_by('?').first()
        print(type(word_obj), '\n\n\n')
        context['word'] = getattr(word_obj, source_lang)
        context['translate'] = getattr(word_obj, translate_lang)
        context['train_id'] = ''
    elif mode == 'user_words':
        cur_train_obj = Train.objects.filter(user=request.user).filter(status='on study').select_related(
            'word').order_by('?').first()
        context['word'] = getattr(cur_train_obj.word, source_lang)
        context['translate'] = getattr(cur_train_obj.word, translate_lang)
        context['train_id'] = cur_train_obj.pk
    elif mode == 'repeat_words':
        cur_train_obj = Train.objects.filter(user=request.user).filter(status='studied').select_related(
            'word').order_by('?').first()
        context['word'] = getattr(cur_train_obj.word, source_lang)
        context['translate'] = getattr(cur_train_obj.word, translate_lang)
        context['train_id'] = cur_train_obj.pk

    context['mode'] = mode
    context['how_translate'] = how_translate

    return render(request, 'new_words/words_text.html', context=context)


@login_required
def words_text_result(request, mode, how_translate):
    word = request.POST['word']

    if how_translate == 'ru-en':
        source_lang = 'russian'
        translate_lang = 'english'
        translates = Word.objects.filter(russian=word).values(f'{translate_lang}')
    else:
        source_lang = 'english'
        translate_lang = 'russian'
        translates = Word.objects.filter(english=word).values(f'{translate_lang}')


    translate_attempt = request.POST['translate_attempt'].strip().lower()
    translate = request.POST['translate']
    train_id = request.POST['train_id']

    is_correct = False
    other_translates_list = []
    for i in translates:
        if i[translate_lang] == translate_attempt:
            is_correct = True
            if train_id:
                cur_train = Train.objects.get(pk=train_id)
                cur_train.correct_ans_cnt += 1
                cur_train.save()
        other_translates_list.append(i[translate_lang])

    if translate_attempt in other_translates_list:
        other_translates_list.remove(translate_attempt)
    if translate in other_translates_list and not is_correct:
        other_translates_list.remove(translate)

    if 'on' in request.POST['studied']:
        cur_train = Train.objects.get(pk=train_id)
        cur_train.status = 'studied'
        cur_train.save()

    context = {
        'word': word,
        'translate_attempt': translate_attempt,
        'translate': translate,
        'is_correct': is_correct,
        'other_translates': other_translates_list,
        'mode': mode,
        'how_translate': how_translate,
    }
    return render(request, 'new_words/words_text_result.html', context=context)

















# ======================================================================================================================
# en -> ru (все слова) перевод текстом

@login_required
def train_words_1(request):
    word = Word.objects.order_by('?').first()
    return render(request, 'new_words/train_words_1.html', context={'word': word})


@login_required
def train_words_1_result(request):
    word = request.POST['word-en'].strip().lower()
    translate = request.POST['translate'].strip().lower()
    right_translate = request.POST['word-ru']

    if right_translate == translate:
        is_correct = True
    else:
        is_correct = False

    context = {
        'word': word,
        'translate': translate,
        'right': right_translate,
        'is_correct': is_correct,
    }
    return render(request, 'new_words/train_words_1_result.html', context=context)


# ======================================================================================================================
# повторение изученных слов

@login_required
def echo_words_en_ru_text(request):
    cur_train = Train.objects.filter(user=request.user).filter(status='studied').select_related('word').order_by('?').first()
    return render(request, 'new_words/echo_words_en_ru_text.html', context={'cur_train': cur_train})


@login_required
def echo_words_en_ru_text_result(request):
    word_en = request.POST['word-en']
    translate_attempt = request.POST['translate'].strip().lower()
    right_translate = request.POST['word-ru']
    train_id = request.POST['train_id']

    translates = Word.objects.filter(english=word_en).values('russian')
    is_correct = False
    other_translates_list = []
    for i in translates:
        if i['russian'] == translate_attempt:
            is_correct = True
            cur_train = Train.objects.get(pk=train_id)
            cur_train.correct_ans_cnt += 1
            cur_train.save()
        other_translates_list.append(i['russian'])

    if translate_attempt in other_translates_list:
        other_translates_list.remove(translate_attempt)
    if right_translate in other_translates_list:
        other_translates_list.remove(right_translate)

    if 'on' in request.POST['stud']:
        cur_train = Train.objects.get(pk=train_id)
        cur_train.status = 'studied'
        cur_train.save()

    context = {
        'word_en': word_en,
        'translate_attempt': translate_attempt,
        'right': right_translate,
        'is_correct': is_correct,
        'other_translates': other_translates_list,
    }
    return render(request, 'new_words/echo_words_en_ru_text_result.html', context=context)


# ======================================================================================================================
# добавление/смена статуса слов

@login_required
def add_words_to_train(request):
    if request.method == 'POST':
        for i in request.POST:
            if i.isdigit():
                word_instance = Word.objects.get(pk=i)
                Train.objects.create(user=request.user, word=word_instance)
    user_words = Train.objects.filter(user=request.user).values('word__english')
    words = Word.objects.exclude(english__in=user_words).order_by('english')
    return render(request, 'new_words/add_words_to_train.html', context={'words': words})
