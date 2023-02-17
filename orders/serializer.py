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
    # product = serializers.DateTimeField()
    price = serializers.IntegerField()
    quantity = serializers.IntegerField()
    # order = serializers.StringRelatedField(many=True)
    # product = serializers.StringRelatedField(many=True)

    class Meta:
        model = OrderItem
        fields = ['order', 'product']
