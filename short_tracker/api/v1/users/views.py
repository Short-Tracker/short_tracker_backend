from django.conf import settings as django_settings
from django.contrib.auth import get_user_model

# from django.http import HttpResponseRedirect
# from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

# from api.v1.users.forms import UploadFileForm
from api.v1.schemas import (
    LOGIN_DONE_SCHEMA,
    LOGIN_SCHEMA,
    LOGOUT_SCHEMA,
    REFRESH_DONE_SCHEMA,
)
from api.v1.users.serializers import (
    AuthSignInSerializer,
    ShortUserSerializer,
)

User = get_user_model()

ACCESS_TOKEN_LIFETIME = int(
    django_settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME', 0).total_seconds()
)
REFRESH_TOKEN_LIFETIME = int(
    django_settings.SIMPLE_JWT.get('REFRESH_TOKEN_LIFETIME', 0).total_seconds()
)


@swagger_auto_schema(
    method='post',
    request_body=LOGIN_SCHEMA,
    responses={
        200: LOGIN_DONE_SCHEMA,
        400: 'Bad request',
    },
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = AuthSignInSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data.get('user')
    access_token = AccessToken.for_user(
        serializer.validated_data.get('user')
    )
    refresh_token = RefreshToken.for_user(
        serializer.validated_data.get('user')
    )
    response = Response(
        ShortUserSerializer(user).data, status=status.HTTP_200_OK
    )
    response.set_cookie(
        'jwt_access', str(access_token), expires=ACCESS_TOKEN_LIFETIME,
        httponly=True, samesite='None', secure=True,
    )
    response.set_cookie(
        'jwt_refresh', str(refresh_token), expires=REFRESH_TOKEN_LIFETIME,
        httponly=True, samesite='None', secure=True,
    )
    return response


@swagger_auto_schema(
    method='post',
    request_body=LOGIN_SCHEMA,
    responses={
        200: REFRESH_DONE_SCHEMA,
        400: 'Bad request',
    },
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refresh_token(request):
    refresh_token = request.COOKIES.get('jwt_refresh')
    refresh = RefreshToken(refresh_token)
    response = Response(
        data={'refresh': ('Токен успешно обновлен!')},
        status=status.HTTP_200_OK
    )
    response.set_cookie(
        'jwt_access', str(refresh.access_token),
        expires=ACCESS_TOKEN_LIFETIME,
        httponly=True, samesite='None', secure=True,
    )

    if django_settings.SIMPLE_JWT.get('ROTATE_REFRESH_TOKENS'):
        refresh.set_jti()
        refresh.set_exp()
        response.set_cookie(
            'jwt_refresh', str(refresh),
            expires=REFRESH_TOKEN_LIFETIME,
            httponly=True, samesite='None', secure=True,
        )

    return response


@swagger_auto_schema(method='post', responses={200: LOGOUT_SCHEMA},)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    response = Response(
        data={'signout': ('Вы успешно вышли из учетной записи!')},
        status=status.HTTP_200_OK
    )
    response.delete_cookie('jwt_access', samesite='None',)
    response.delete_cookie('jwt_refresh', samesite='None',)

    return response


# def add_photo(request):
#     response = Response(
#         data={'signout': ('Вы успешно вышли из учетной записи!')},
#         status=status.HTTP_200_OK
#     )
#     response.


# def add_photo(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             # return HttpResponseRedirect('/success/url/')
#     # else:
#     #     form = UploadFileForm()
#     return render(request, 'poll/articles.html', {'form': form})
