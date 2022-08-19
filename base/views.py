from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required



def main_page(request):
    return render(request, 'base/main_page.html', context={})


@login_required
def trainer(request):
    return render(request, 'base/trainer.html')