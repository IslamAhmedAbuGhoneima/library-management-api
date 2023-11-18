from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    book = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['auther', 'title', 'description', 'pages', 'price', 'available',
                  'no_of_rate', 'avg_rate', 'publication_date']


class AuthorSerializer(serializers.ModelSerializer):
    auther_books = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Auther
        fields = ['id', 'name', 'biography', 'auther_books']


class UserSerializer(serializers.ModelSerializer):
    user_books = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_books']


class SingupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
