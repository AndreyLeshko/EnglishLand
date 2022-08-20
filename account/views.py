from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from new_words.models import Train


@login_required
def personal_page(request):
    words_cnt = Train.objects.filter(user=request.user).values('status').annotate(count=Count('status')).order_by('status')

    print('\n\n\n')
    print(words_cnt)

    context = {}

    if not words_cnt:
        context['on_study'] = 0
        context['studied'] = 0
    else:
        context['on_study'] = words_cnt[0]['count']
        context['studied'] = words_cnt[1]['count']
    return render(request, 'account/personal_page.html', context=context)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            # user_profile = Profile(user=new_user)
            # user_profile.save()
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


