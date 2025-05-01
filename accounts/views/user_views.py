from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from accounts.serializers import *
from accounts.models import Role
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from accounts.filters import UserFilter
from commons.pagination import Pagination

User = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        role_name_or_id = request.data.get('role', '')

        # Handle role as either name or ID
        try:
            if isinstance(role_name_or_id, str):
                role_name_or_id = role_name_or_id.strip().upper()
                role = Role.objects.get(name=role_name_or_id)
            else:
                role = Role.objects.get(pk=role_name_or_id)

            user.role = role
            user.save()
        except Role.DoesNotExist:
            return Response({'error': f"Role '{role_name_or_id}' does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': "Invalid role value."}, status=status.HTTP_400_BAD_REQUEST)

        tokens = get_tokens_for_user(user)

        return Response({
            'user': serializer.data,
            'role': user.role.name if user.role else None,
            'tokens': tokens
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    serializer = TokenObtainPairSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def token_refresh_view(request):
    """Refresh the access token."""
    serializer = TokenRefreshSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def reset_password(request):
    email = request.data.get('email')
    new_password = request.data.get('new_password')

    if not email or not new_password:
        return Response({'error': 'Email and new password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)
	
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST.name])
def getAllUserWithoutPagination(request):
	users = User.objects.all()

	serializer = UserListSerializer(users, many=True)

	return Response({'users': serializer.data}, status=status.HTTP_200_OK)





@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getAUser(request, pk):
	try:
		user = User.objects.get(pk=pk)
		serializer = UserSerializer(user)
		return Response(serializer.data)
	except ObjectDoesNotExist:
		return Response({'detail': f"User id - {pk} doesn't exists"})




@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def searchUser(request):
	users = UserFilter(request.GET, queryset=User.objects.all())
	users = users.qs

	print('searched_products: ', users)

	total_elements = users.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	users = pagination.paginate_data(users)

	serializer = UserListSerializer(users, many=True)

	response = {
		'users': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(users) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no users matching your search"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request, pk):
	try:
		user = User.objects.get(pk=pk)
		data = request.data
		serializer = UserSerializer(user, data=data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		return Response({'detail': f"User id - {pk} doesn't exists"})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteUser(request, pk):
	try:
		user = User.objects.get(pk=pk)
		user.delete()
		return Response({'detail': f'User id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"User id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)