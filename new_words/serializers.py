from rest_framework import serializers

from .models import WordEnglish


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordEnglish
        fields = ['pk', 'english']