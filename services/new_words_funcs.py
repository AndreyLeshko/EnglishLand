from django.core.exceptions import ObjectDoesNotExist

from random import choice

from new_words.models import Train, Vocabulary, WordEnglish, WordRussian, WordCategory


def get_train_word_object(request, is_studied: bool) -> Train:
    """
        Возвращает объект модели Train (со статусом изучено/не изучено) с вероятностью выпадания согласно приоритету
        Номер приоритета - Вероятность выдачи слова с данным приоритетом
        1 - 12%
        2 - 16%
        3 - 20%
        4 - 24%
        5 - 28%
    """
    priorities = [1] * 3 + [2] * 4 + [3] * 5 + [4] * 6 + [5] * 7
    random_priority = choice(priorities)
    cur_train_obj = Train.objects \
        .filter(user=request.user).filter(is_studied=is_studied).filter(priority=random_priority) \
        .select_related('word').prefetch_related('word__translates').order_by('last_try', '?').first()
    # если в бд нет слова с нужным приоритетом, выбираем с приоритетом на 1 меньше:
    while not cur_train_obj and random_priority > 1:
        random_priority -= 1
        cur_train_obj = Train.objects \
            .filter(user=request.user).filter(is_studied=is_studied).filter(priority=random_priority) \
            .select_related('word').prefetch_related('word__translates').order_by('last_try', '?').first()
    if not cur_train_obj:
        cur_train_obj = Train.objects.filter(user=request.user).filter(is_studied=is_studied) \
            .select_related('word').prefetch_related('word__translates').order_by('last_try', '?').first()
    return cur_train_obj


def get_new_words_for_user(user):
    """Возвращает список слов, которые пока не были добавлены пользователем для изучения"""
    user_words = Train.objects.filter(user=user).values('word__english')
    new_words = WordEnglish.objects.exclude(english__in=user_words).order_by('english').values('english')
    return new_words


def get_category_list():
    """Возвращает список категорий слов"""
    categories = WordCategory.objects.all()
    return categories


def add_new_word_to_db(english: str, russian: str, category_name: str):
    """Добавляет в бд новое слово и его переводы"""
    category_obj = WordCategory.objects.get(category_name=category_name)
    try:
        word_en = WordEnglish.objects.get(english=english)
    except ObjectDoesNotExist:
        word_en = WordEnglish(english=english)
        word_en.save()

    translates = [word.lower().strip() for word in russian.split(';')]  # т.к. вводится несколько переводов через ";"
    for translate in translates:
        try:
            word_ru = WordRussian.objects.get(russian=translate)
        except ObjectDoesNotExist:
            word_ru = WordRussian(russian=translate)
            word_ru.save()
        Vocabulary.objects.create(english=word_en, russian=word_ru, category=category_obj)


def update_priority(train_id: int) -> None:
    """Пересчитывает значение приоритета"""
    cur_train = Train.objects.get(pk=train_id)
    correct_ans_percent = cur_train.correct_ans_cnt / (cur_train.incorrect_ans_cnt + cur_train.correct_ans_cnt) * 100

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
    cur_train.priority = new_priority
    cur_train.save()


def check_is_it_train_owner(username, train_id):
    train_obj = Train.objects.get(pk=train_id)
    if username == train_obj.user.username:
        return True
    return False


def translates_dict(train_obj):
    ru_translates_obj = train_obj.word.translates.all()
    context = {
        'english': train_obj.word.english,
        'russian': {}
    }
    for ru_translate_obj in ru_translates_obj:
        en_translates = [translate['english'] for translate in ru_translate_obj.translates.all().values('english')]
        context['russian'][ru_translate_obj.russian] = en_translates
    return context
