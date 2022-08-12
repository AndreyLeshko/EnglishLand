from django.shortcuts import render
from rest_framework import generics
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Word, Train
from .serializers import WordSerializer


# ======================================================================================================================
# API

class WordsAPIView(generics.ListAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer


# ======================================================================================================================
# перевод текстом en->ru / ru->en
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
# добавление/смена статуса слов

@login_required
def add_words_to_train(request):
    if request.method == 'POST':
        print(request.POST)
        print('\n\n\n')
        for i in request.POST:
            if 'on' in request.POST[i]:
                word_instance = Word.objects.filter(english=i).first()
                Train.objects.create(user=request.user, word=word_instance)
        #     if i.isdigit():
        #         word_instance = Word.objects.get(pk=i)
        #         Train.objects.create(user=request.user, word=word_instance)
    user_words = Train.objects.filter(user=request.user).values('word__english')
    new_words = Word.objects.exclude(english__in=user_words).order_by('english').values('english').distinct()
    paginator = Paginator(new_words, 20)
    page = request.GET.get('page')
    try:
        words = paginator.page(page)
    except PageNotAnInteger:
        words = paginator.page(1)
    except EmptyPage:
        words = paginator.page(paginator.num_pages)
    # print(words.paginator.num_pages)
    # print('\n\n\n')
    return render(request, 'new_words/add_words_to_train.html', context={'words': words, 'page': page})
