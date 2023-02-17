from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User,Address


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name')


    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('passwords dont match')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="you can change password using <a href=\"../password/\">this form</a>.")

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name', 'password', 'last_login')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'



class UserRegistrationForm(forms.Form):

    email = forms.EmailField(widget=forms.TextInput({'class': 'f1', 'placeholder': 'Enter email *'}), label=False)
    full_name = forms.CharField(widget=forms.TextInput({'class': 'f1', 'placeholder': 'Enter fullname *'}), label=False)
    phone = forms.CharField(widget=forms.TextInput({'class': 'f1', 'placeholder': 'Enter phone number *'}), label=False)
    password = forms.CharField(widget=forms.PasswordInput({'class': 'f1', 'placeholder': 'Enter password *'}),
                               label=False, )

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email already exists')
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        user = User.objects.filter(phone_number=phone).exists()
        if user:
            raise ValidationError('This phone number already exists')
        # OtpCode.objects.filter(phone_number=phone).delete()
        return phone


class VerifyCodeForm(forms.Form):
    code = "success"


class UserLoginForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput({'class':'f1','placeholder': 'Enter phone number *'}),label=False)
    password = forms.CharField(widget=forms.PasswordInput({'class':'f1','placeholder': 'Enter password *'}),label=False,)

class addAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields ='__all__'
class updateUserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput({'class': 'f1', 'placeholder': 'Enter email *'}))
    full_name = forms.CharField(widget=forms.TextInput({'class': 'f1', 'placeholder': 'Enter fullname *'}))
    phone = forms.CharField(widget=forms.TextInput({'class': 'f1', 'placeholder': 'Enter phone number *'}))
    password = forms.CharField(widget=forms.PasswordInput({'class': 'f1', 'placeholder': 'Enter password *'})
                               )

    class Meta:
        model = User
        fields =[]



