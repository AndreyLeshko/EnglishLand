from django.contrib.auth.models import User
from rest_framework import serializers

from .models import WordEnglish, Train


class WordSerializer(serializers.ModelSerializer):

    class Meta:
        model = WordEnglish
        fields = ['english']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk']


class WordTrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = ['word', 'user', 'correct_ans_cnt', 'incorrect_ans_cnt', 'priority']


class TrainObjectSerializer(serializers.ModelSerializer):
    word = WordSerializer()
    user = UserSerializer()

    class Meta:
        model = Train
        fields = ['word', 'user', 'priority', 'id']