from rest_framework import serializers
from users.models import User, UserBio


class UserSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(source='userbio.bio', required=False)
    role = serializers.CharField(source='userbio.role', required=False)

    class Meta:
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        )
        model = User
        extra_kwargs = {
            'email': {'required': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'A user with that email already exists.'
            )
        return value

    def create(self, validated_data):
        user_bio_data = validated_data.pop('userbio', {})
        user = User.objects.create_user(
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            email=validated_data['email'],
            username=validated_data['username']
        )
        UserBio.objects.create(
            user=user,
            bio=user_bio_data.get('bio', ''),
            role=user_bio_data.get('role', 'user')
        )
        if user.userbio.role == 'moderator':
            user.is_staff = True
            user.save()
        elif user.userbio.role == 'admin':
            user.is_superuser = True
            user.is_staff = True
            user.save()
        return user
