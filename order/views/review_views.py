from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from order.models import Review
from order.serializers import ReviewSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createReview(request):
    serializer = ReviewSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(customer=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def listProductReviews(request, product_id):
    reviews = Review.objects.filter(product_id=product_id)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)
