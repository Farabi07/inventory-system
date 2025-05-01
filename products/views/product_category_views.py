from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers, status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response

from products.models import ProductCategory
from products.serializers import *
from products.filters import ProductCategoryFilter

from commons.pagination import Pagination
from rest_framework.permissions import IsAuthenticated

# Create your views here.
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllProductCategory(request):
	categories=ProductCategory.objects.all()
	total_elements = categories.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	categories.paginate_data(categories)

	serializer = ProductCategoryListSerializer(categories, many=True)

	response = {
		'product_categories': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	return Response(response, status=status.HTTP_200_OK)




@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllProductCategoryWithoutPagination(request):
	categories  =ProductCategory.objects.all()

	serializer = ProductCategoryListSerializer(categories, many=True)

	return Response({'categories': serializer.data}, status=status.HTTP_200_OK)



@api_view(['GET'])
def getAProductCategory(request, pk):
	try:
		categories   = ProductCategory.objects.get(pk=pk)
		serializer = ProductCategoryListSerializer(categories, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"ProductCategory id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PRODUCT_DETAILS.name])
def searchProductCategory(request):

	categories = ProductCategoryFilter(request.GET, queryset=ProductCategory.objects.all())
	categories = categories.qs

	print('categories: ', categories)

	total_elements = categories.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	categories = pagination.paginate_data(categories)

	serializer = ProductCategoryListSerializer(categories, many=True)

	response = {
		'categories': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(categories) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no categories matching your search"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductCategory(request):
	data = request.data
	print('data: ', data)

	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != '0':
			filtered_data[key] = value

	name = filtered_data.get('name', None)
	if name is not None:
		try:
			name = str(name).upper()
			categories = ProductCategory.objects.get(name=name)
			return Response({'detail': f"ProductCategory with name '{name}' already exists."})
		except ProductCategory.DoesNotExist:
			pass

	serializer = ProductCategorySerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateProductCategory(request,pk):
	try:
		categories = ProductCategory.objects.get(pk=pk)
		data = request.data
		serializer = ProductCategorySerializer(categories, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		return Response({'detail': f"ProductCategory id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DELETE.name])
@api_view(['DELETE'])
def deleteProductCategory(request, pk):
	try:
		categories = ProductCategory.objects.get(pk=pk)
		categories.delete()
		return Response({'detail': f'ProductCategory id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"ProductCategory id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
