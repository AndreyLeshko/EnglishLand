from django.urls import path

from . import views


app_name = 'base'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('trainer/', views.trainer, name='trainer'),
]
