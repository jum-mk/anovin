from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User

class TutorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutorial
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
