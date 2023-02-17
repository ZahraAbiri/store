import random

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect,get_object_or_404
from django.views import View

from .forms import UserRegistrationForm, VerifyCodeForm, UserLoginForm, addAddressForm, updateUserForm
from .models import User, Address


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register111.html'

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
            User.objects.create_user(user_session['phone_number'], user_session['email'], user_session['full_name'],
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
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'info')
                return redirect('products:products')
            messages.error(request, 'phone or password is wrong', 'warning')
        return render(request, self.template_name, {'form': form})


def addressList(request):
    id = request.user.id
    print(id)
    address = Address.objects.raw('SELECT * FROM accounts_address where customer_id="%s"' % id)
    # address = Address.objects.get(Customer_id=id)
    print(address)
    return render(request, "accounts/address-list.html", {'address': address})


# request.user
# discount = Coupon.objects.all()
# return render(request, "home/discount-list.html", {'discount': discount})


def addressCreate(request):
    if request.method == "POST":
        form = addAddressForm(request.POST)
        if form.is_valid():
            model = form.instance
            form.save(model)
            return redirect('accounts:addresslist')
    else:
        form = addAddressForm()
    return render(request, 'accounts/address-create.html', {'form': form})


def update_address(request, id):
    context = {}
    obj = get_object_or_404(Address, id=id)
    form = addAddressForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('accounts:addresslist')
    context["form"] = form
    return render(request, "accounts/address-update.html", context)
def profileUpdate(request):
    context = {}
    obj = get_object_or_404(Address, id=request.user.id)
    form = updateUserForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/')
    context["form"] = form
    return render(request, "accounts/profile-update.html", context)


def delete_address(request, id):
    context = {}
    obj = get_object_or_404(Address, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect("accounts:addresslist")

    return render(request, "accounts/delete_address.html", context)
