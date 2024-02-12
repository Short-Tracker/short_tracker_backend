import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def user_1(django_user_model):
    return django_user_model.objects.create(
        email='user_1@egmail.com',
        password='password123',
        first_name='Иван',
        last_name='Иванов',
        telegram_nickname='@ivanov',
        is_team_lead=False,
    )


@pytest.fixture
def team_lead_user(django_user_model):
    return django_user_model.objects.create(
        email='teamlead@gmail.com',
        password='password321',
        first_name='Алексей',
        last_name='Алексеев',
        telegram_nickname='@team_lead',
        is_team_lead=True,
    )

@pytest.fixture
def team_lead_token(team_lead_user):
    refresh = RefreshToken.for_user(team_lead_user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@pytest.fixture
def performer_token(user_1):
    refresh = RefreshToken.for_user(user_1)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@pytest.fixture
def team_lead_client(team_lead_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {team_lead_token["access"]}')
    return client

@pytest.fixture
def performer_client(performer_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {performer_token["access"]}')
    return client
