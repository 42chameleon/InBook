from django.conf import settings
import tempfile
from django.db.models import Count, Case, When, F
from book.serializers import BookSerializer
from django.contrib.auth.models import User
from django.core.files import File
from django.urls import reverse
from rest_framework.test import APITestCase
from book.models import Book, Category
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.exceptions import ErrorDetail


class BooksApiTestCase(APITestCase):
    def setUp(self):
        settings.MEDIA_ROOT = tempfile.mkdtemp()
        self.category = Category.objects.create(name='test_category')
        self.user = User.objects.create(username='test username')
        file_name = 'starik_i_more.pdf'
        file = File(open('uploads/starik_i_more.pdf', 'rb'))
        uploaded_file = SimpleUploadedFile(
            file_name, file.read(), content_type='multipart/from-data')
        self.book = Book.objects.create(name='test_book',
                                        author_name='test_author',
                                        book_file=uploaded_file,
                                        owner=self.user,
                                        category=self.category)

    def test_get(self):
        url = reverse('book-list')
        books = Book.objects.all().annotate(
            owner_name=F('owner__username'),
            category_name=F('category__name'),
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))
        ).prefetch_related('readers').order_by('-id')
        response = self.client.get(url)
        serializer_data = BookSerializer(books, many=True).data
        response.data[0]['book_file'] = serializer_data[0]['book_file']
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_create(self):
        self.assertEqual(1, Book.objects.all().count())
        file_name = 'starik_i_more.pdf'
        file = File(open('uploads/starik_i_more.pdf', 'rb'))
        uploaded_file = SimpleUploadedFile(
            file_name, file.read(), content_type='multipart/from-data')
        self.client.force_login(user=self.user)
        data = {
            "name": "test_name",
            "author_name": "test_author",
            "book_file": uploaded_file,
            "category": self.category.name
        }
        url = reverse('book-list')
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(2, Book.objects.all().count())

    def test_update(self):
        url = reverse('book-detail', args=(self.book.id,))
        self.client.force_login(user=self.user)
        data = {
            "name": "Test_Book",
            "author_name": "test_book_author",
            "book_file": self.book.book_file,
            "category": self.category.name
        }
        self.client.force_login(self.user)
        response = self.client.put(url, data, format='multipart')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book.refresh_from_db()
        self.assertEqual('test_book_author', self.book.author_name)

    def test_update_not_owner(self):
        self.user1 = User.objects.create(username='test user1')
        url = reverse('book-detail', args=(self.book.id,))
        data = {
            "name": self.book.name,
            "author_name": "test_book_author1",
            "book_file": self.book.book_file,
            "category": self.category.name
        }
        self.client.force_login(self.user1)
        response = self.client.put(url, data, format='multipart')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.book.refresh_from_db()
        self.assertEqual("test_author", self.book.author_name)
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')}, response.data)

    def test_update_not_owner_but_staff(self):
        url = reverse('book-detail', args=(self.book.id,))
        data = {
            "name": self.book.name,
            "author_name": "test_book_author1",
            "book_file": self.book.book_file,
            "category": self.category.name
        }
        self.user1 = User.objects.create(username='test user1', is_staff=True)
        self.client.force_login(self.user1)
        response = self.client.put(url, data, format='multipart')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book.refresh_from_db()
        self.assertEqual("test_book_author1", self.book.author_name)
