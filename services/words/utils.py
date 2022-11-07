from new_words.models import WordEnglish, Train


class WordsReview:

    def __init__(self, filters, user_id=None):
        self.filters = filters
        self.user_id = user_id
        self.queryset = None

    def filter_by_status(self, status: str):
        if not self.user_id:
            return
        if status == 'new':
            self.queryset = self.queryset.filter(trains__id__isnull=True)
        elif status == 'studied':
            self.queryset = self.queryset.filter(trains__is_studied=True)
        elif status == 'on_study':
            self.queryset = self.queryset.filter(trains__is_studied=False)

    def filter_by_categories(self, categories: list):
        self.queryset = self.queryset.filter(vocabulary__category__category_name__in=categories)

    def filter_by_tags(self, tags: list):
        pass

    def get_queryset(self):
        self.queryset = WordEnglish.objects.all().distinct()

        filter_funcs = {
            'categories': self.filter_by_categories,
            'status': self.filter_by_status,
            'tags': self.filter_by_tags,
        }
        for filter_ in self.filters:
            filter_funcs[filter_](self.filters[filter_])
        return self.queryset
