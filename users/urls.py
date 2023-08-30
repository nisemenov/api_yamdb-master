from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UsersViewSet, send_confirmation, send_token


router = DefaultRouter()
router.register(r'users', UsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/email/', send_confirmation),
    path('auth/token/', send_token),
]
