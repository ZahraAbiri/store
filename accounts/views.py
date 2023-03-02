import random

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View, csrf
from rest_framework import status, views, permissions
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from orders.cart import Cart, CART_SESSION_ID
from orders.forms import CartAddForm
from orders.models import Order, Coupon
from products.models import Product, Category
from .forms import UserRegistrationForm, VerifyCodeForm, UserLoginForm, addAddressForm, updateUserForm, \
    User_RegistrationForm
from .models import User, Address
from .serializer import UserSerializer


class UserRegisterView(View):
    # todo is addmin or just customer
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            # send_otp_code(form.cleaned_data['phone'], random_code)
            # OtpCode.objects.create(phone_number=form.cleaned_data['phone'], code=random_code)
            request.session['user_registration_info'] = {
                'phone_number': form.cleaned_data['phone'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password': form.cleaned_data['password'],
            }
            user_session = request.session['user_registration_info']
            User.objects.create_customer(user_session['phone_number'], user_session['email'], user_session['full_name'],
                                     user_session['password'])
            messages.success(request, 'you registered.', 'success')
            # messages.success(request, 'we sent you a code', 'success')
            # return redirect('products:home')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form': form})


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/verify.html', {'form': form})


# def post(self, request):
# 	user_session = request.session['user_registration_info']
# 	code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
# 	form = self.form_class(request.POST)
# 	if form.is_valid():
# 		cd = form.cleaned_data
# 		if cd['code'] == code_instance.code:
# 			User.objects.create_user(user_session['phone_number'], user_session['email'],
# 									 user_session['full_name'], user_session['password'])
#
# 			code_instance.delete()
# 			messages.success(request, 'you registered.', 'success')
# 			return redirect('home:home')
# 		else:
# 			messages.error(request, 'this code is wrong', 'danger')
# 			return redirect('accounts:verify_code')
# 	return redirect('home:home')


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out successfully', 'success')
        return redirect('products:products')


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        print(str(request.session.session_key))
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        key = request.session
        print(str(request.session.get(CART_SESSION_ID)) + "---")

        # cart = copy.deepcopy(Cart(request).cart)
        # logout(request)
        # session = request.session
        # session[CART_SESSION_ID] = cart
        # session.modified = True
        # todo

        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # request.session.session_key=key
            user = authenticate(request, phone_number=cd['phone'], password=cd['password'])
            # print('authenticate' + request.session.session_key)

            if user is not None:
                # print('before login' + request.session.session_key)
                # print('before login'+str(cart.Cart))

                login(request, user)
                # url=request.get('next')
                # settp
                cart = Cart(request)
                product = get_object_or_404(Product, id=1)
                form = CartAddForm(request.POST)
                if form.is_valid():
                    cart.add(product, form.cleaned_data['quantity'])
                messages.success(request, 'you logged in successfully', 'info')
                if str(request.session.get(CART_SESSION_ID))=='{}':
                    return redirect('products:products')

                else:
                    return redirect('orders:cart')


            messages.error(request, 'phone or password is wrong', 'warning')
        return render(request, self.template_name, {'form': form})


def addressList(request):
    id = request.user.id
    print(id)
    address = Address.objects.filter(customer_id=id)
    # address = Address.objects.get(Customer_id=id)
    print(address)
    return render(request, "accounts/address-list.html", {'address': address})
def addressListManagement(request):
    address = Address.objects.all()
    print(address)
    return render(request, "accounts/address-list.html", {'address': address})

class loginView(views.APIView):
    # authentication_classes = (AllowAny,)
    def post(self, request,format=None):
        data=request.data
        username=data.get('phone_number')
        password=data.get('password')
        print(username,password)
        user=authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                messages.success(request, 'you login successfully.')
                return Response('you login successfully.')
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


# request.user
# discount = Coupon.objects.all()
# return render(request, "home/discount-list.html", {'discount': discount})


def addressCreate(request):
    if request.method == "POST":
          # this is the added line
        form = addAddressForm(request.POST)
        if form.is_valid():
            print('valid')
            model = form.instance
            form.save(model)
            return redirect('accounts:addressListManagement')
    else:
        form = addAddressForm()
    return render(request, 'accounts/address-create.html', {'form': form})


def update_address(request, id):
    obj = get_object_or_404(Address, id=id)
    form = addAddressForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('accounts:addressListManagement')
    form = addAddressForm()
    return render(request, "accounts/address-update.html", {'form': form})


def profileUpdate(request):
    # context = {}
    obj = get_object_or_404(User, id=request.user.id)
    form = updateUserForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/')
    # context["form"] = form
    form = updateUserForm()

    return render(request, "accounts/profile-update.html", {'obj': obj, 'form': form})


def delete_address(request, id):
    context = {}
    obj = get_object_or_404(Address, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect("accounts:addressListManagement")

    return render(request, "accounts/delete_address.html", context)


def nazer_panel(request):
    list_product = Product.objects.all()
    list_Order = Order.objects.all()
    list_user = User.objects.all()
    list_category = Category.objects.all()
    list_address = Address.objects.all()
    list_discount = Coupon.objects.all()

    return render(request, "accounts/nazer.html", {'product': list_product, 'discount': list_discount,
                                                   'order': list_Order, 'user': list_user,
                                                   'category': list_category, 'address': list_address})





def Operator_user_create(request):
    if request.method == "POST":

        form = User_RegistrationForm(request.POST)
        if form.is_valid():
            print(request.POST.get('is_customer'))
            # print(form.is_customer)
            # print(form.is_admin)
            # print(form.is_operator)
            # print(form.is_nazer)
            request.session['user_registration_info'] = {
                'phone_number': form.cleaned_data['phone'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password': form.cleaned_data['password'],
            }
            user_session = request.session['user_registration_info']
            if request.POST.get('is_customer'):
                User.objects.create_customer(user_session['phone_number'], user_session['email'], user_session['full_name'],
                                         user_session['password'])
            elif request.POST.get('is_operator'):
                User.objects.create_operator(user_session['phone_number'], user_session['email'],
                                             user_session['full_name'],
                                             user_session['password'])
            elif request.POST.get('is_nazer'):
                User.objects.create_nazer(user_session['phone_number'], user_session['email'],
                                             user_session['full_name'],
                                             user_session['password'])
            else:
                User.objects.create_superuser(user_session['phone_number'], user_session['email'],
                                             user_session['full_name'],
                                             user_session['password'])
            messages.success(request, 'you registered.', 'success')
            # form.save()
            return redirect('accounts:userlist')
    else:
        form = User_RegistrationForm()
    return render(request, 'operator/user-create.html', {'form': form})
#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             random_code = random.randint(1000, 9999)

#             return redirect('accounts:verify_code')
#         return render(request, self.template_name, {'form': form})

def update_Operator_user_(request, id):
    context = {}
    obj = get_object_or_404(User, id=id)
    form = updateUserForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('accounts:userlist')
    context["form"] = form
    return render(request, "operator/user-update.html", context)
def operator_user_List(request):
    user = User.objects.all()
    return render(request, "operator/user-list.html", {'user': user})

def delete_user_operator(request, id):
    context = {}
    obj = get_object_or_404(User, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect("accounts:userlist")

    return render(request, "operator/delete_user.html", context)

def customerAddAddress(request):
    if request.method == "POST":
        post = request.POST
        print(str(post))
        c=post['city_name']
        a=post['avenue_name']
        s=post['street_name']
        p=post['plate']
        z=post['zipCode']
        u=request.user.id
        add=Address(city_name=c,avenue_name=a,street_name=s,plate=p,zipCode=z,customer_id=u)
        Address.save(add)
        return redirect("accounts:addresslist")
    return render(request, "accounts/userAddAddress.html")
