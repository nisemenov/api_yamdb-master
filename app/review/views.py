from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, filters

from django_filters.rest_framework import DjangoFilterBackend

from review.models import Review, Comment, Title, Genre, Category
from review.serializers import (
    ReviewSerializer,
    CommentSerializer,
    TitleSerializerList,
    TitleSerializerDetail,
    GenreSerializer,
    CategorySerializer
)
from review.permissions import IsSuperuserOrRead, IsOwnerOrReadOnly
from review.filters import TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    )
    filter_backends = [filters.OrderingFilter]
    ordering_field = ['id']
    ordering = ['id']

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.review.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    )
    filter_backends = [filters.OrderingFilter]
    ordering_field = ['id']
    ordering = ['id']

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = get_object_or_404(
            title.review.all(),
            pk=self.kwargs.get('review_id')
        )
        return review.comment.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsSuperuserOrRead)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = TitleFilter
    ordering_field = ['id', 'name']
    ordering = ['-id']

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleSerializerList
        return TitleSerializerDetail


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsSuperuserOrRead)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    lookup_field = 'slug'
    ordering_field = ['id']
    ordering = ['id']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsSuperuserOrRead)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    lookup_field = 'slug'
    ordering_field = ['id']
    ordering = ['id']
