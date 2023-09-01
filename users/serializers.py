from rest_framework import serializers
from users.models import User, UserBio


class UserSerializer(serializers.ModelSerializer):
    bio = serializers.ReadOnlyField(source='userbio.bio')
    role = serializers.ReadOnlyField(source='userbio.role')


    class Meta:
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        )
        model = User
