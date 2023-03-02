from django.shortcuts import get_object_or_404
from rest_framework import status, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from orders.models import OrderItem, Order
from orders.serializer import OrderItemSerializer
from products.models import CartItem, Product
from products.serializer import CartItemSerializer


class CartItemViews(APIView):
    def post(self, request):
        quantity = request.data.get('quantity')
        user_id = request.data.get('user_id')
        products_id = request.data.get('products_id')
        price = request.data.get('price')
        order_id = request.data.get('order_id')
        u = User.objects.get(pk=user_id)
        p = Product.objects.get(pk=products_id)
        print(type(u))
        print(str(p))
        if quantity !='' and user_id !='' and products_id !='' and order_id !='':
            order = Order(user=u)
            Order.save(order)
            item = OrderItem(product=p, order=order, quantity=quantity, price=price)
            OrderItem.save(item)
            print('sjhfosihfewohi')
            return Response('added', status=status.HTTP_200_OK)
        else:
            return Response("error", status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id:
            item = OrderItem.objects.get(id=id)
            serializer = OrderItemSerializer(item)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

        items = OrderItem.objects.all()
        serializer = OrderItemSerializer(items, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, id=None):
        quantity = request.data.get('quantity')
        user_id = request.data.get('user_id')
        products_id = request.data.get('products_id')
        price = request.data.get('price')

        if quantity !='' or user_id !='' or products_id !='':
            item = Order.objects.get(id=id)
            item.user_id = user_id
            Order.save(item)
            order_item = OrderItem.objects.get(order_id=item.id)
            order_item.price = price
            order_item.quantity = quantity
            order_item.product_id = products_id
            OrderItem.save(order_item)
            return Response('update')
        else:
            return Response('error')

    def delete(self, request, id=None):
        # id = request.data.get('order_id')
        o = Order.objects.get(pk=id)
        print(str(o))
        o.delete()
        return Response({"data": "Item Deleted"})




#  "data": {
#         "products_id": "1",
#
#         "price": 530,
#         "quantity": 4,
#         "user_id": "1",
#
#     }


@api_view(['POST'])
def update_items(request, pk):
    item = CartItem.objects.get(pk=pk)
    data = CartItemSerializer(instance=item, data=request.data)

    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

