from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F

from new_words.models import Train, Vocabulary, WordEnglish, WordRussian, WordCategory


def get_random_word() -> Vocabulary:
    """Возвращает случайный объект модели Vocabulary"""
    word_obj = Vocabulary.objects.order_by('?').first()
    return word_obj


def get_train_word_object(request, is_studied: bool) -> Train:
    """Возвращает объект модели Train (со статусом изучено/не изучено)"""
    cur_train_obj = Train.objects.filter(user=request.user).filter(is_studied=is_studied) \
        .select_related('word').prefetch_related('word__translates').order_by('last_try', '?').first()
    return cur_train_obj


def get_possible_translations(word: str, how_translate: str) -> list:
    """Возвращает список переводов заданного слова"""
    if how_translate == 'ru-en':
        translates = [i.english.english for i in Vocabulary.objects.filter(russian__russian=word)]
    else:
        translates = [i.russian.russian for i in Vocabulary.objects.filter(english__english=word)]
    return translates


def add_word_to_train(user, how_translate: str, word: str) -> None:
    """Создаёт объект модели Train для выбранного пользователем слова"""
    if how_translate == 'ru-en':
        word_instance = Vocabulary.objects.select_related('russian').filter(russian__russian=word).first().english
    else:
        word_instance = WordEnglish.objects.get(english=word)
    Train.objects.create(user=user, word=word_instance)


def change_status_is_studied(train_id: int, new_status: bool) -> None:
    """Меняет статус is_studied модели Train"""
    cur_train = Train.objects.get(pk=train_id)
    cur_train.is_studied = new_status
    cur_train.save()


def increase_counter_right_answers(train_id: int) -> None:
    """Увеличивает счетчик правильных ответов на единницу"""
    cur_train = Train.objects.get(pk=train_id)
    cur_train.correct_ans_cnt += 1
    cur_train.save()


def update_train_last_try(train_id: int) -> None:
    """Обновляет дату последней попытки"""
    cur_train = Train.objects.get(pk=train_id)
    cur_train.save()


def get_translation_variants(cur_train_obj: Train, how_translate: str) -> list:
    """Возвращает список из трех вариантов перевода"""
    if how_translate == 'ru-en':
        variants_obj = Vocabulary.objects.filter(category=cur_train_obj.word.vocabulary.first().category)\
            .exclude(english=cur_train_obj.word).order_by('?').values(word=F('english__english')).distinct()[:3]
    else:
        variants_obj = Vocabulary.objects.filter(category=cur_train_obj.word.vocabulary.first().category) \
            .exclude(english=cur_train_obj.word).order_by('?').values(word=F('russian__russian'))[:3]
    variants_list = [variant['word'] for variant in variants_obj]
    return variants_list


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
