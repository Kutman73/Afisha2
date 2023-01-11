from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import *


class UserAuthorizationAPIView(APIView):
    def post(self, request):
        serializer = UserValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, create = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED,
                        data={'error': 'User not found!'})


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserCreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User.objects.create_user(**serializer.data)
        return Response(status=status.HTTP_201_CREATED)
