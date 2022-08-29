from django.urls import path

from . import views


app_name = 'base'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('trainer/', views.trainer, name='trainer'),
    path('section_in_development/', views.section_in_development, name='section_in_development'),
]
