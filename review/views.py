from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, filters

from django_filters.rest_framework import DjangoFilterBackend

from review.models import Review, Comment, Title, Genre, Category
from review.serializers import (
    ReviewSerializer,
    CommentSerializer,
    TitleSerializer,
    GenreSerializer,
    CategorySerializer
)
from review.permissions import IsSuperuserOrRead
from review.filters import TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.review

    # permission_classes = (IsOwnerObj,)
    # filter_backends = (DjangoFilterBackend,)
    # filterset_fields = ('group',)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = get_object_or_404(
            title.review,
            pk=self.kwargs.get('review_id')
        )
        return review.comment


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsSuperuserOrRead,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsSuperuserOrRead,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'
