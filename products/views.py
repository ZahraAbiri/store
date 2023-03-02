# from . import tasks
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

# from utils import IsAdminUserMixin
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from orders.cart import Cart
from orders.forms import CartAddForm
from orders.models import Coupon, Order
from .forms import addProForm, addCategoryForm, addDiscountForm
from .models import Product, Category, CartItem
from .serializer import CartItemSerializer


class HomeView(View):
    def get(self, request, category_slug=None):
        cart = Cart(request)
        print()
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        return render(request, 'home/home.html', {'products': products, 'categories': categories, 'cart': len(cart)})


class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)

        if product.discount is not None:
            x = product.discount * 0.01
            y = product.price * x
            z = product.price - (y)
            product.price = z
            print(product.price)
        form = CartAddForm()
        return render(request, 'home/detail.html', {'product': product, 'form': form})


class IsAdminUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin


# class BucketHome(IsAdminUserMixin, View):
#     template_name = 'home/bucket.html'
#
#     def get(self, request):
#         # objects = tasks.all_bucket_objects_task()
#         return render(request, self.template_name)
#
#
# class DeleteBucketObject(IsAdminUserMixin, View):
#     def get(self, request, key):
#         # tasks.delete_object_task.delay(key)
#         messages.success(request, 'your object will be delete soon.', 'info')
#         return redirect('home:bucket')
#
#
# class DownloadBucketObject(IsAdminUserMixin, View):
#     def get(self, request, key):
#         # tasks.download_object_task.delay(key)
#         messages.success(request, 'your download will start soon.', 'info')
#         return redirect('home:bucket')
class my_form(View):
    def get(self, request):
        return render(request, 'home/addProduct.html', )

    def post(self, request):
        form = addProForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            form = addProForm()
            return render(request, 'home/addProduct.html', {'form': form})


def productList(request):
    # print(id)
    products = Product.objects.all()
    return render(request, "home/product-list.html", {'products': products})


def categoryList(request):
    # print(id)
    category = Category.objects.all()
    return render(request, "home/category-list.html", {'category': category})


def discountList(request):
    # print(id)
    discount = Coupon.objects.all()
    return render(request, "home/discount-list.html", {'discount': discount})


def productCreate(request):
    if request.method == "POST":
        form = addProForm(request.POST, request.FILES)

        try:
            print("igriutirutury")

            if form.is_valid():
                try:
                    model = form.instance
                    form.save(model)
                    return redirect('products:productlist')
                except:
                    pass
        except Exception as e:
            # raise Exception as e:
            print(e)
    else:
        form = addProForm()
    return render(request, 'home/product-create.html', {'form': form})


def categoryCreate(request):
    if request.method == "POST":
        form = addCategoryForm(request.POST)
        print('cateeeee')
        try:
            print("igriutirutury")

            if form.is_valid():
                try:
                    model = form.instance
                    form.save(model)
                    return redirect('products:categorylist')
                except:
                    pass
        except Exception as e:
            # raise Exception as e:
            print(e)
    else:
        form = addCategoryForm()
    return render(request, 'home/category-create.html', {'form': form})


def discountCreate(request):
    if request.method == "POST":
        form = addDiscountForm(request.POST)
        print('cateeeee')
        try:
            print("igriutirutury")

            if form.is_valid():
                try:
                    model = form.instance
                    print("utourotureit")
                    form.save(model)
                    print("hjdfjhdhfshdj")
                    return redirect('products:discountlist')
                except:
                    pass
        except Exception as e:
            # raise Exception as e:
            print(e)
    else:
        form = addDiscountForm()
    return render(request, 'home/discount-create.html', {'form': form})


def create_view(request):
    context = {}
    form = addProForm(request.POST or None)
    if form.is_valid():
        form.save()
        print('saaasasasaaaaaaaaaaaaa')
    else:
        print("jjjjjjjjjj")
    context['form'] = form
    return render(request, "home/product-create.html", context)


def productUpdate(request, id):
    product = Product.objects.get(id=id)
    form = addProForm(initial={'category': product.category,
                               'name': product.name,
                               'image': product.image,
                               'description': product.description,
                               'price': product.price,
                               })
    if request.method == "POST":
        form = addProForm(request.POST, instance=product)
        if form.is_valid():
            try:
                model = form.instance
                form.save(model)
                return redirect('productlist/list/')
            except Exception as e:
                print(e)
    return render(request, 'home/product-update.html', {'form': form})


def delete_view(request, id):
    context = {}
    obj = get_object_or_404(Product, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect("products:productlist")

    return render(request, "home/delete_view.html", context)


def delete_category(request, id):
    context = {}
    obj = get_object_or_404(Category, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect("products:categorylist")

    return render(request, "home/delete_category.html", context)
def delete_discount(request, id):
    context = {}
    obj = get_object_or_404(Coupon, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect("products:discountlist")

    return render(request, "home/delete_discount.html", context)


def update_view(request, id):
    context = {}
    obj = get_object_or_404(Product, id=id)
    form = addProForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('products:productlist')
    context["form"] = form
    return render(request, "home/product-update.html", context)


def update_category(request, id):
    context = {}
    obj = get_object_or_404(Category, id=id)
    form = addCategoryForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('products:categorylist')
    context["form"] = form
    return render(request, "home/category-update.html", context)


def update_discount(request, id):
    context = {}
    obj = get_object_or_404(Coupon, id=id)
    form = addDiscountForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('products:discountlist')
    context["form"] = form
    return render(request, "home/discount-update.html", context)



@api_view(['POST'])
def add_items(request):
    item = CartItemSerializer(data=request.data)

    # validating for already existing data
    if CartItem.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    if item.is_valid():
        item.save()
        return Response(item.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def view_items(request):
    # checking for the parameters from the URL
    if request.query_params:
        items = CartItem.objects.filter(**request.query_params.dict())
    else:
        items = CartItem.objects.all()

    # if there is something in items else raise error
    if items:
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def update_items(request, pk):
    item = CartItem.objects.get(pk=pk)
    data = CartItemSerializer(instance=item, data=request.data)

    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
# @api_view(['DELETE'])
# def delete_items(request, pk):
#     item = get_object_or_404(Order, pk=pk)
#     item.delete()
#     return Response(status=status.HTTP_202_ACCEPTED)
