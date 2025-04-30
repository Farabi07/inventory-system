from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.decorators import api_view
from rest_framework import status

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }
@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()  
        print(serializer.data['username'])
        role_value = request.data.get('role', 'user')
        tokens = get_tokens_for_user(user)  
        return Response({
            'user': serializer.data,  
            'tokens': tokens
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    serializer = TokenObtainPairSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def token_refresh_view(request):
    """ Refresh the access token """
    serializer = TokenRefreshSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def reset_password(request):
    email = request.data.get('email')
    new_password = request.data.get('new_password')

    try:
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)
    



