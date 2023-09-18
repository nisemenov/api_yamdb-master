from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UsersViewSet, SendConfirmationCode, SendToken


router = DefaultRouter()
router.register(r'users', UsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/email/', SendConfirmationCode.as_view()),
    path('auth/token/', SendToken.as_view()),
]
