from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    """Сериализатор для пользователей"""

    class Meta:
        model = User
        fields = (
            'username', 'telegram_nickname', 'email',
            'first_name', 'last_name', 'role'
        )
        read_only_fields = ('role',)
