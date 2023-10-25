from rest_framework import serializers
from .models import Article, Reminder, Source


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = '__all__'


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'
