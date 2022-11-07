from django.contrib.auth.models import User
from rest_framework import serializers

from .models import WordEnglish, WordRussian, Train, Vocabulary


class WordEnSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordEnglish
        fields = ['id', 'english']


class WordRuSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordRussian
        fields = ['id', 'russian']


class VocabularySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.category_name')
    russian = WordRuSerializer()

    class Meta:
        model = Vocabulary
        fields = ['russian', 'category']


class WordReviewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    english = serializers.CharField()
    details = serializers.CharField(source='get_absolute_url')
    # details = serializers.HyperlinkedRelatedField(view_name='words:words_detail', read_only=True)
    status = serializers.CharField(source='trains.first.get_status', allow_null=True)
    vocabulary = VocabularySerializer(source='vocabulary.all', many=True)

    class Meta:
        model = WordEnglish
        fields = ['id', 'english', 'details', 'status', 'vocabulary']


class WordEnHyperlinkSerializer(serializers.ModelSerializer):
    # details = WordEnglish

    class Meta:
        model = WordEnglish
        fields = ['id', 'english']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk']


class WordTrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = ['word', 'user', 'correct_ans_cnt', 'incorrect_ans_cnt', 'priority']


class TrainObjectSerializer(serializers.ModelSerializer):
    word = WordEnHyperlinkSerializer(read_only=True)

    class Meta:
        model = Train
        fields = ['word', 'priority', 'id', 'is_studied']
