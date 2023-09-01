from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework import viewsets, permissions

from users.models import User, UserBio
from users.serializers import UserSerializer
from users.permissions import IsSuperuser

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from random import randint as ri

from rest_framework_simplejwt.tokens import RefreshToken


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

    def get_object(self):
        if self.kwargs['username'] == 'me':
            return self.request.user
        return super().get_object()


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def send_confirmation(request):
    try:
        email = request.query_params['email']
        user = get_object_or_404(
            User,
            email=email
        )
    except MultiValueDictKeyError:
        return Response(
            {'This field is required': 'email'},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        user.userbio
    except ObjectDoesNotExist:
        UserBio.objects.create(user=user)
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
    confirmation_code = ri(0, 99999999)
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
            email=request.query_params['email'],
            userbio__confirmation_code=
            request.query_params['confirmation_code']
        )
        return Response({'token': get_tokens_for_user(user)['access']})
    except MultiValueDictKeyError as e:
        return Response(
            f'You forgot this field: {e}',
            status=status.HTTP_400_BAD_REQUEST
        )
