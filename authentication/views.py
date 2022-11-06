from django.shortcuts import render
from rest_framework.generics import CreateAPIView, GenericAPIView
from authentication.serializers import LoginSerializer, UserSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class RegisterView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer

class LoginView(GenericAPIView):
    # the login function will generate a token use the token with the use of postman agent to view other api.
    permission_classes = ()
    serializer_class = LoginSerializer
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token":user.auth_token.key})
        return Response({"errorr": "wrong credentials"}, status = status.HTTP_400_BAD_REQUEST)
