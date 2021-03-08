from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from book.models import Book, UserBookRelation, Profile, Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


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


class ProfileSerializer(serializers.Serializer):
    book_id = serializers.IntegerField(read_only=True)
    name_book = serializers.CharField(read_only=True)
    category_name = serializers.CharField(read_only=True)
    user_owner = serializers.StringRelatedField(read_only=True)
    annotated_likes = serializers.IntegerField(read_only=True)
    book_url = serializers.SerializerMethodField()
    user_name = serializers.CharField(read_only=True)
    user_surname = serializers.CharField(read_only=True)

    class Meta:
        model = Profile
        fields = (
            'book_id',
            'user', 'user_name', 'user_surname', 'relation', 'book_url', 'user_owner', 'annotated_likes',
            'category_name',
            'name_book')

    def get_book_url(self, book):
        request = self.context.get('request')
        book_url = book.book_file.url
        return request.build_absolute_uri(book_url)
