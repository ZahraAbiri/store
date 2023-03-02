from rest_framework import serializers

from .models import Order, OrderItem


# class OrderSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Order
#         fields = ['user', 'paid', 'created', 'groups', 'discount']
#
#
# class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ['order', 'product', 'price', 'quantity']

class OrderSerializer(serializers.Serializer):
    paid = serializers.BooleanField(default=False)
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()
    discount = serializers.IntegerField()
class OrderItemSerializer(serializers.Serializer):
    # order = serializers.Fo(default=False)
    products_id = serializers.CharField(source='product.id', read_only=True)
    products_name = serializers.CharField(source='product.name', read_only=True)
    price = serializers.IntegerField()
    quantity = serializers.IntegerField()
    user_id = serializers.CharField(source='order.user.id', read_only=True)
    order_id = serializers.CharField(source='order.id', read_only=True)
    # product = serializers.StringRelatedField(many=True)

    class Meta:
        model = OrderItem
        fields = ['user_id','quantity','price','products_name','order_id','products_id']
