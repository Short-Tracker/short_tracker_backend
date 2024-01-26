from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    """Serializer for user registration."""

    class Meta:
        model = User
        fields = (
            'email', 'username', 'telegram_nickname',
            'password', 'first_name', 'last_name',
            'is_team_lead'
        )


class UserSerializer(serializers.ModelSerializer):
    """Serializer for users."""

    class Meta:
        model = User
        fields = (
            'id', 'username', 'telegram_nickname', 'email',
            'first_name', 'last_name', 'is_team_lead'
        )


class ShortUserSerializer(serializers.ModelSerializer):
    """Serializer for short representation of users."""

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'full_name', 'telegram_nickname', 'email', 'is_team_lead'
        )

    def get_full_name(self, obj):
        """
        Get the full name of an object or return the nickname of telegram.
        """

        if obj.last_name and obj.first_name:
            return f'{obj.first_name} {obj.last_name[:1]}.'
        return 'ФИО не указано.'


class AuthSignInSerializer(serializers.Serializer):
    """Serializer for user login."""

    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate(self, data):
        try:
            user = User.objects.get(email=data.get('email'))
        except User.DoesNotExist:
            raise NotFound(
                detail={'email': ('Пользователь с таким email не существует')},
            )
        else:
            if user.check_password(data.get("password")):
                data['user'] = user
                return data
            raise ValidationError(
                detail={'password': ('Неверный пароль')},
            )
