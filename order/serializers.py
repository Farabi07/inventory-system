from rest_framework import serializers
from .models import Order, OrderItem, Review
from products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = OrderItem
        fields = ['product_id', 'quantity', 'price_at_purchase']
        read_only_fields = ['price_at_purchase']

    def create(self, validated_data):
        product = Product.objects.get(id=validated_data['product_id'])
        quantity = validated_data['quantity']

        if product.stock_quantity < quantity:
            raise serializers.ValidationError(f"Not enough stock for {product.name}")

        product.stock_quantity -= quantity
        product.save()

        validated_data['product'] = product
        validated_data['price_at_purchase'] = product.price
        return super().create(validated_data)

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ['id', 'customer', 'status', 'total_amount', 'items', 'created_at']
        read_only_fields = ['total_amount', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        total = 0
        for item_data in items_data:
            item_serializer = OrderItemSerializer(data=item_data)
            item_serializer.is_valid(raise_exception=True)
            order_item = item_serializer.save(order=order)
            total += order_item.price_at_purchase * order_item.quantity

        order.total_amount = total
        order.save()
        return order


class SalesInvoiceSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.full_name') 
    customer_email = serializers.EmailField(source='customer.email')
    items = OrderItemSerializer(many=True)  

    class Meta:
        model = Order
        fields = [
            'id',
            'status',
            'created_at',
            'customer_name',
            'customer_email',
            'items',
            'total_price', 
        ]
class ReviewSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'product', 'product_name', 'customer_name', 'rating', 'comment', 'created_at']
