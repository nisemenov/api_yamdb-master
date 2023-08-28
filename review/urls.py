from django.urls import path, include
from rest_framework.routers import DefaultRouter
from review.views import (
    ReviewViewSet,
    TitleViewSet,
    CommentViewSet,
    GenreViewSet,
    CategoryViewSet
)


router = DefaultRouter()
router.register(r'titles', TitleViewSet)
router.register(
    r'titles/(?P<title_id>[^/.]+)/reviews',
    ReviewViewSet,
    basename='reviews')
router.register(
    r'titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments',
    CommentViewSet,
    basename='comments')
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
