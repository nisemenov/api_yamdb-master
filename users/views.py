from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework import viewsets, permissions

from users.models import UserBio
from users.serializers import UserSerializer
from users.permissions import IsSuperuser

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.mail import send_mail
from random import randint as ri

from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
    }


class UsersViewSet(viewsets.ModelViewSet):
    queryset = UserBio.objects.all()
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
        user = UserBio.objects.get(email=email)
        if user.confirmation_code:
            send_mail(
                'Confirmation code YaMBd',
                f"You've already logged into YaMBd, "
                f"this is your confirmation code:\n "
                f"{user.confirmation_code}.",
                None,
                [email, ]
            )
            return Response(
                {'email': email},
                status=status.HTTP_200_OK
            )
        confirmation_code = ri(0, 99999999)
        user.confirmation_code = confirmation_code
        user.save()
        send_mail(
            'Confirmation code YaMBd',
            f"You've logged into YaMBd, this is your confirmation code:\n "
            f"{confirmation_code}.",
            None,
            [email, ]
        )
        return Response(
                {'email': email},
                status=status.HTTP_200_OK
            )
    except UserBio.DoesNotExist:
        return Response(
            {'message': f'There is no user with such email: '
                        f'[{request.query_params["email"]}]!'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except MultiValueDictKeyError:
        return Response(
            {'message': f'Email field is required!'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def send_token(request):
    try:
        user = get_object_or_404(
            UserBio,
            email=request.query_params['email'],
            confirmation_code=request.query_params['confirmation_code']
        )
        return Response({'token': get_tokens_for_user(user.user)['access']})
    except MultiValueDictKeyError as e:
        return Response(
            f'You forgot this field: {e}',
            status=status.HTTP_400_BAD_REQUEST
        )
