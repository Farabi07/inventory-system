from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from order.models import Order
from order.serializers import OrderSerializer
from commons.pagination import Pagination
from django.db.models import Q
from accounts.models import User
from products.models import Product
from order.permissions import IsCustomerOrReadOnly, IsAdminOrSeller


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getAllOrders(request):
    orders = Order.objects.all()
    total_elements = orders.count()

    page = request.query_params.get('page')
    size = request.query_params.get('size')

    pagination = Pagination()
    pagination.page = page
    pagination.size = size
    orders = pagination.paginate_data(orders)

    serializer = OrderSerializer(orders, many=True)

    response = {
        'orders': serializer.data,
        'page': pagination.page,
        'size': pagination.size,
        'total_pages': pagination.total_pages,
        'total_elements': total_elements,
    }

    return Response(response, status=status.HTTP_200_OK)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getAnOrder(request, pk):
    try:
        order = Order.objects.get(pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'detail': f"Order id - {pk} doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsCustomerOrReadOnly])
def createOrder(request):
    data = request.data
    serializer = OrderSerializer(data=data, context={'request': request})

    if serializer.is_valid():
        # Check stock availability before saving the order
        for item_data in data.get('items', []):
            product_id = item_data.get('product')
            quantity = item_data.get('quantity')

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({'detail': f"Product ID {product_id} not found."}, status=status.HTTP_400_BAD_REQUEST)

            if product.stock < quantity:
                return Response({'detail': f"Not enough stock for {product.name}. Available: {product.stock}"}, status=status.HTTP_400_BAD_REQUEST)

        # Save the order (creates Order and OrderItems)
        order = serializer.save()

        # Deduct stock
        for item in order.items.all():  # Assuming related_name='items'
            product = item.product
            product.stock -= item.quantity
            product.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrSeller])
def searchOrders(request):
    customer_id = request.query_params.get('customer')
    product_id = request.query_params.get('product')
    status = request.query_params.get('status')
    date = request.query_params.get('date')

    filters = Q()
    if customer_id:
        filters &= Q(customer__id=customer_id)
    if product_id:
        filters &= Q(items__product__id=product_id)
    if status:
        filters &= Q(status__iexact=status)
    if date:
        filters &= Q(created_at__date=date)

    orders = Order.objects.filter(filters).distinct()
    total_elements = orders.count()

    page = request.query_params.get('page')
    size = request.query_params.get('size')

    pagination = Pagination()
    pagination.page = page
    pagination.size = size
    orders = pagination.paginate_data(orders)

    serializer = OrderSerializer(orders, many=True)

    response = {
        'orders': serializer.data,
        'page': pagination.page,
        'size': pagination.size,
        'total_pages': pagination.total_pages,
        'total_elements': total_elements,
    }

    if total_elements > 0:
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response({'detail': "No matching orders found"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminOrSeller])
def updateOrder(request, pk):
    try:
        order = Order.objects.get(pk=pk)
        data = request.data

        serializer = OrderSerializer(order, data=data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except ObjectDoesNotExist:
        return Response({'detail': f"Order id - {pk} doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminOrSeller])
def deleteOrder(request, pk):
    try:
        order = Order.objects.get(pk=pk)
        order.delete()
        return Response({'detail': f'Order id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'detail': f"Order id - {pk} doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSalesInvoice(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
        serializer = OrderSerializer(order)  # Assuming nested serializer includes OrderItems

        invoice_data = {
            'order_id': order.id,
            'customer': {
                'name': order.customer.full_name,
                'email': order.customer.email,
                'phone': order.customer.phone_number
            },
            'order_date': order.created_at.strftime("%d-%m-%Y"),
            'status': order.status,
            'total_price': order.total_price,  # ensure you calculate this in model or serializer
            'items': [
                {
                    'product': item.product.name,
                    'quantity': item.quantity,
                    'unit_price': item.price,
                    'total': item.quantity * item.price
                }
                for item in order.items.all()
            ]
        }

        return Response(invoice_data, status=status.HTTP_200_OK)

    except Order.DoesNotExist:
        return Response({'detail': f"Order ID {order_id} not found"}, status=status.HTTP_404_NOT_FOUND)
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure only authenticated users can access this
def getSalesHistory(request):
    # Extract query params for filtering
    customer_id = request.query_params.get('customer')
    product_id = request.query_params.get('product')
    status = request.query_params.get('status')
    date = request.query_params.get('date')

    filters = Q()  # Start with an empty filter

    # Apply filters based on the query parameters provided
    if customer_id:
        filters &= Q(customer__id=customer_id)
    if product_id:
        filters &= Q(items__product__id=product_id)
    if status:
        filters &= Q(status__iexact=status)  # Case-insensitive match for status
    if date:
        filters &= Q(created_at__date=date)  # Filter by exact date

    # Apply the filters to the Order model
    orders = Order.objects.filter(filters).distinct()  # Ensure unique results
    
    total_elements = orders.count()  # Get the total number of filtered orders

    # Pagination parameters
    page = request.query_params.get('page')
    size = request.query_params.get('size')

    # Set up pagination
    pagination = Pagination()
    pagination.page = page
    pagination.size = size
    orders = pagination.paginate_data(orders)  # Apply pagination

    # Serialize the order data
    serializer = OrderSerializer(orders, many=True)

    response = {
        'orders': serializer.data,
        'page': pagination.page,
        'size': pagination.size,
        'total_pages': pagination.total_pages,
        'total_elements': total_elements,
    }

    # Return the response with the filtered and paginated data
    return Response(response, status=status.HTTP_200_OK)