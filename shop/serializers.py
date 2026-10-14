from rest_framework import serializers

from shop.models import Order, OrderItem, Product


class ProductSerializer(serializers.Serializer):
    # TODO 1: khai báo field: id (chỉ đọc), name (tối đa 200 ký tự), price (10 chữ số, 2 số thập phân)

    def validate_price(self, value):
        # TODO 2: price phải > 0, nếu không thì raise serializers.ValidationError
        if (value <= 0):
            raise serializers.ValidationError 
        return value

    def create(self, validated_data):
        # TODO 3: tạo Product từ validated_data
        ...


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["product_name", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    # TODO 4: customer_email lấy từ customer.email (chỉ đọc), items lồng OrderItemSerializer

    class Meta:
        model = Order
        fields = ["id", "status", "created_at", "customer_email", "items"]
