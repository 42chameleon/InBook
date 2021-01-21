from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return f'ID {self.id}: {self.name}'


class Book(models.Model):
    name = models.CharField(max_length=300)
    author_name = models.CharField(max_length=300)
    book_file = models.FileField(upload_to='uploads/')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='my_book')
    readers = models.ManyToManyField(User, through='UserBookRelation', related_name='books')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'ID {self.id}: {self.name}'


class UserBookRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Ok'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False, blank=True)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True, blank=True)

    def __str__(self):
        return f' user: {self.user}, {self.book}, rate: {self.rate}'


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='book', on_delete=models.SET_NULL, null=True)
    relation = models.ForeignKey(UserBookRelation, on_delete=models.SET_NULL, null=True)
