from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator as dtg

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import UserSerializer
from users.permissions import IsSuperuserOrOwner


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
    }


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperuserOrOwner)
    lookup_field = 'username'
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter
    ]
    filterset_fields = ['username']
    search_fields = ['username']
    ordering_fields = ['username']
    ordering = ['username']

    def get_object(self):
        if self.kwargs['username'] == 'me':
            return self.request.user
        return super().get_object()

    def destroy(self, request, *args, **kwargs):
        if self.kwargs['username'] == 'me':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request)


class SendConfirmationCode(APIView):
    def post(self, request):
        email = request.data.get('email', None)
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            user.email_user(
                'Confirmation code YaMBd',
                f"You've already logged into YaMBd, "
                f"this is your new confirmation code:\n"
                f"{dtg.make_token(user)}."
            )
            return Response({'email': email},
                            status=status.HTTP_201_CREATED)

        serializer = UserSerializer(data={
            'email': request.data.get('email', None),
            'username': request.data.get('email', None)
        }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.instance
        user.email_user(
            'Confirmation code YaMBd',
            f"You've just logged into YaMBd, this is your confirmation code:\n"
            f"{dtg.make_token(user)}."
        )
        return Response({'email': email}, status=status.HTTP_201_CREATED)


class SendToken(APIView):
    def post(self, request):
        email = request.data.get('email', None)
        confirmation_code = request.data.get('confirmation_code', None)
        user = get_object_or_404(User, email=email)
        if dtg.check_token(user, confirmation_code):
            return Response({'token': get_tokens_for_user(user)['access']},
                            status=status.HTTP_200_OK)
        return Response(
            'Confirmation code is not valid.',
            status=status.HTTP_400_BAD_REQUEST
        )
