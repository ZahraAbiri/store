from rest_framework import serializers
from .models import CartItem
class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    product_quantity = serializers.IntegerField(required=False, default=1)

    class Meta:
        model = CartItem
        fields = ['product_id','user_id','product_quantity']