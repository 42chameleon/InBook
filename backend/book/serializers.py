from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from book.models import Book, UserBookRelation


class BookSerializer(ModelSerializer):
    owner_name = serializers.CharField(read_only=True)
    category_name = serializers.CharField(read_only=True)
    annotated_likes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'name', 'author_name', 'owner_name', 'readers', 'category_name', 'annotated_likes', 'book_file')


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'in_bookmarks', 'rate')
