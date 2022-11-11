from django.db.models import Q, Value, Case, When, FilteredRelation, CharField, F, Count, IntegerField

from new_words.models import WordEnglish


class WordsReview:
    def __init__(self, filters, user_id=None):
        self.filters = filters
        self.user_id = user_id
        self.queryset = None

    def filter_by_status(self, status: str):
        if not self.user_id:
            return
        if status == 'new':
            self.queryset = self.queryset.filter(train_status='null')
        elif status == 'studied':
            self.queryset = self.queryset.filter(train_status='studied')
        elif status == 'on_study':
            self.queryset = self.queryset.filter(train_status='on_study')

    def filter_by_categories(self, categories: list):
        self.queryset = self.queryset.filter(vocabulary__category__category_name__in=categories)

    def filter_by_tags(self, tags: list):
        pass

    def get_queryset(self):
        self.queryset = WordEnglish.objects \
            .prefetch_related('trains') \
            .prefetch_related('vocabulary__category') \
            .annotate(user_train=FilteredRelation('trains', condition=Q(trains__user__pk=self.user_id))) \
            .annotate(train_status=Case(
                When(Q(user_train__isnull=True), then=Value('null')),
                When(Q(user_train__is_studied=True), then=Value('studied')),
                When(Q(user_train__is_studied=False), then=Value('on_study')),
                output_field=CharField())
            ).order_by('english').all().distinct()

        filter_funcs = {
            'categories': self.filter_by_categories,
            'status': self.filter_by_status,
            'tags': self.filter_by_tags,
        }
        for filter_ in self.filters:
            filter_funcs[filter_](self.filters[filter_])
        return self.queryset
