from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from services import account_funcs


def main_page(request):
    context = {}
    if request.user.is_authenticated:
        context.update(account_funcs.get_user_words_statistic(request.user))
    return render(request, 'base/main_page.html', context=context)


@login_required
def trainer(request):
    return render(request, 'base/trainer.html')