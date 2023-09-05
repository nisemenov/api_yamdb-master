from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework import viewsets, permissions, filters

from users.models import User, UserBio
from users.serializers import UserSerializer
from users.permissions import IsSuperuser

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from random import randint as ri

from rest_framework_simplejwt.tokens import RefreshToken

from django_filters.rest_framework import DjangoFilterBackend


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
    }


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSuperuser,)
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


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def send_confirmation(request):
    try:
        email = request.data['email']
        user = get_object_or_404(
            User,
            email=email
        )
    except KeyError:
        return Response(
            {'email': 'This field is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    if user.userbio.confirmation_code:
        send_mail(
            'Confirmation code YaMBd',
            f"You've already logged into YaMBd, "
            f"this is your confirmation code:\n "
            f"{user.userbio.confirmation_code}.",
            None,
            [email, ]
        )
        return Response(
            {'email': email},
            status=status.HTTP_200_OK
        )
    confirmation_code = ri(100000, 99999999)
    user.userbio.confirmation_code = confirmation_code
    user.userbio.save()
    send_mail(
        'Confirmation code YaMBd',
        f"You've just logged into YaMBd, this is your confirmation code:\n "
        f"{confirmation_code}.",
        None,
        [email, ]
    )
    return Response(
            {'email': email},
            status=status.HTTP_200_OK
        )


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def send_token(request):
    try:
        user = get_object_or_404(
            User,
            email=request.data['email'],
            userbio__confirmation_code=
            request.data['confirmation_code']
        )
        return Response({'token': get_tokens_for_user(user)['access']})
    except KeyError as e:
        return Response(
            {'error': f'{e} field is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
