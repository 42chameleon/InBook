from rest_framework.viewsets import ModelViewSet
from django.db.models import Count, Case, When, F
from book.permissions import IsOwnerOrStaffOrReadOnly
from book.serializers import BookSerializer
from book.models import Book


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
