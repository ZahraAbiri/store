import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Address
from .cart import Cart
from .forms import CartAddForm, CouponApplyForm, orderItemForm
from .models import Order, OrderItem, Coupon
from .models import Product
from .serializer import OrderSerializer, OrderItemSerializer


# import requests

class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart.html', {'cart': cart})


class CartAddView(View):
    # todo kkkkkkkkkkkkk

    print('permision_required')

    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('orders:cart')


# @api_view
class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('orders:cart')


class OrderDetailView(LoginRequiredMixin, View):
    form_class = CouponApplyForm

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        id = request.user.id
        address = Address.objects.filter(customer_id=id)
        return render(request, 'orders/order.html', {'order': order, 'form': self.form_class, 'address': address})


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                     quantity=item['quantity'])
        cart.clear()
        return redirect('orders:order_detail', order.id)


class OrderPayView(LoginRequiredMixin, View):
    # permission_required = 'orders.add_order'
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        request.session['order_pay'] = {
            'order_id': order.id,
        }
        order.paid = True
        order.sent_status = True
        order.save()
        return redirect('/')


class OrderVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        order_id = request.session['order_pay']['order_id']
        order = Order.objects.get(id=int(order_id))
        # t_status = request.GET.get('Status')
        # t_authority = request.GET['Authority']
        if request.GET.get('Status') == 'OK':
            req_header = {"accept": "application/json",
                          "content-type": "application/json'"}

        else:
            return HttpResponse('Transaction failed or canceled by user')


class CouponApplyView(LoginRequiredMixin, View):
    form_class = CouponApplyForm

    def post(self, request, order_id):
        now = datetime.datetime.now()
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            except Coupon.DoesNotExist:
                messages.error(request, 'this coupon does not exists', 'danger')
                return redirect('orders:order_detail', order_id)
            order = Order.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()
        return redirect('orders:order_detail', order_id)


# -----------------
class OrderView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        persons = Order.objects.all()
        ser_data = OrderSerializer(instance=persons, many=True)
        return Response(data=ser_data.data)


# class OrderItemListView(APIView):
#     throttle_scope = 'orderItem'
#
#     def get(self, request):
#         questions = OrderItem.objects.all()
#         srz_data = OrderItemSerializer(instance=questions, many=True).data
#         return Response(srz_data, status=status.HTTP_200_OK)

@api_view()
def showAllOrders(request):
    home = Order.objects.all()
    serializer = OrderSerializer(instance=home, many=True)
    return Response(data=serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def show(request, pk):
    home = Order.objects.all()
    serializer = OrderSerializer(instance=home, many=True)
    # return Response(data=serializer.data)

    try:
        snippet = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrderSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OrderSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def showAllOrderItems(request):
    home = OrderItem.objects.all()
    serializer = OrderItemSerializer(instance=home, many=True)
    return Response(data=serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def showOrderItemView(request, pk):
    home = OrderItem.objects.all()
    serializer = OrderSerializer(instance=home, many=True)
    # return Response(data=serializer.data)

    try:
        snippet = OrderItem.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrderItemSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OrderItemSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    # class OrderItemCreateView(APIView):
    #     """
    #         Create a new question
    #     """
    #     permission_classes = [IsAuthenticated, ]
    #     serializer_class = OrderItemSerializer
    #
    #     def post(self, request):
    #         srz_data = OrderItemSerializer(data=request.data)
    #         if srz_data.is_valid():
    #             srz_data.save()
    #             return Response(srz_data.data, status=status.HTTP_201_CREATED)
    #         return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    #
    # class QuestionUpdateView(APIView):
    #     permission_classes = [IsOwnerOrReadOnly, ]
    #
    #     def put(self, request, pk):
    #         question = OrderItem.objects.get(pk=pk)
    #         self.check_object_permissions(request, question)
    #         srz_data = OrderItem(instance=question, data=request.data, partial=True)
    #         if srz_data.is_valid():
    #             srz_data.save()
    #             return Response(srz_data.data, status=status.HTTP_200_OK)
    #         return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    #
    # class QuestionDeleteView(APIView):
    #     permission_classes = [IsOwnerOrReadOnly, ]
    #
    #     def delete(self, request, pk):
    #         question = OrderItem.objects.get(pk=pk)
    #         question.delete()
    #         return Response({'message': ' deleted'}, status=status.HTTP_200_OK)
    # class OrderList(mixins.RetrieveModelMixin,
    #                     mixins.UpdateModelMixin,
    #                     mixins.DestroyModelMixin,
    #                     generics.GenericAPIView):
    #     """
    #     List all orders, or create a new snippet.
    #     """
    #     # serializer_class = OrganisationDetailSerializer
    #     queryset = Order.objects.all()
    #     serializer_class = OrderSerializer
    #     lookup_field = 'orderview'
    #
    #
    #     def get(self, request, *args, **kwargs):
    #         return self.retrieve(request, *args, **kwargs)
    #
    #     def put(self, request, *args, **kwargs):
    #         return self.update(request, *args, **kwargs)
    #
    #     def delete(self, request, *args, **kwargs):
    #         return self.destroy(request, *args, **kwargs)
    #     # def get_object(self, pk):
    #     #     try:
    #     #         return Order.objects.get(pk=pk)
    #     #     except Order.DoesNotExist:
    #     #         raise Http404
    #     #
    #     # def get(self, request, pk, format=None):
    #     #     snippet = self.get_object(pk)
    #     #     serializer = OrderSerializer(snippet)
    #     #     return Response(serializer.data)
    #     #
    #     # def put(self, request, pk, format=None):
    #     #     snippet = self.get_object(pk)
    #     #     serializer = OrderSerializer(snippet, data=request.data)
    #     #     if serializer.is_valid():
    #     #         serializer.save()
    #     #         return Response(serializer.data)
    #     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     #
    #     # def delete(self, request, pk, format=None):
    #     #     snippet = self.get_object(pk)
    #     #     snippet.delete()
    #     #     return Response(status=status.HTTP_204_NO_CONTENT)


from itertools import chain


def orderHistoryList(request):
    id = request.user.id
    order = OrderItem.objects.select_related('order').filter(order__user_id=id).select_related('product')
    return render(request, "orders/orderHistory.html", {'order': order})


def orderStatusList(request):
    id = request.user.id
    order = OrderItem.objects.select_related('order').filter(order__user_id=id).select_related('product')
    return render(request, "orders/orderStatus.html", {'order': order})

def orderItemUpdate(request, id):
    context = {}
    obj = get_object_or_404(OrderItem, id=id)
    form = orderItemForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('accounts:userlist')
    context["form"] = form
    return render(request, "orders/order-update.html", context)
def order_List(request):
    order = OrderItem.objects.all()
    return render(request, "orders/order-list.html", {'order': order})

def orderItemDelete(request, id):
    context = {}
    obj = get_object_or_404(OrderItem, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect("orders:order_List")

    return render(request, "orders/delete_order.html", context)

def orderItemcreate(request):
    if request.method == "POST":
        form = orderItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('orders:order_List')
    else:
        form = orderItemForm()
    return render(request, 'orders/create-order.html', {'form': form})


def getAllProduct(request):
    products =Product.objects.all()
    for i in products:
        if i.discount is not None:
            x=i.discount*0.01
            y=i.price*x
            z=i.price-(y)
            i.price=z
            print(i.price)
        else:
            continue
    for i in products:
        print(i.price)
    return render(request,'orders/create-order.html')


