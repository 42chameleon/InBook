from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django.db.models import Count, Case, When, F
from book.permissions import IsOwnerOrStaffOrReadOnly
from book.serializers import BookSerializer, UserBookRelationSerializer, ProfileSerializer
from book.models import Book, UserBookRelation


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all().annotate(
        owner_name=F('owner__username'),
        category_name=F('category__name'),
        annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))
    ).prefetch_related('readers').order_by('-id')
    serializer_class = BookSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class UserBookRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    lookup_field = 'book'

    def get_object(self):
        obj, _ = UserBookRelation.objects.get_or_create(user=self.request.user, book_id=self.kwargs['book'])
        return obj


class ProfileView(ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]

    def get_queryset(self):
        user = self.request.user.id
        return Book.objects.filter(owner=user).annotate(
            book_id=F('id'),
            name_book=F('name'),
            user_owner=F('owner__username'),
            user_name=F('owner__first_name'),
            user_surname=F('owner__last_name'),
            category_name=F('category__name'),
            book_url=F('book_file'),
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))
        )


class ProfileLikeOrSaveBook(ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]

    def get_queryset(self):
        user = self.request.user.id
        return Book.objects.filter(readers=user).annotate(
            book_id=F('id'),
            name_book=F('name'),
            user_owner=F('owner__username'),
            category_name=F('category__name'),
            book_url=F('book_file'),
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))
        )
