from django import forms
import datetime
from orders.models import Coupon
from .models import Product, Category


class addProForm(forms.ModelForm):
    # category = forms.ModelMultipleChoiceField(Category, related_name='products')
    # name = forms.CharField(max_length=200)
    # slug = forms.CharField(max_length=200)
    # image = forms.ImageField()
    # description =forms.CharField(widget=forms.Textarea)
    # price = forms.IntegerField()
    available = forms.NullBooleanField()

    class Meta:
        model = Product
        fields = [
            "category",
            "name",
            "slug",
            "price",
            #     "available",
            "image",
            "description",
        ]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for myField in self.fields:
    #         self.fields[myField].widget.attrs['class'] = 'form-control'


class addCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['is_sub', 'name', 'slug', 'sub_category']


class addDiscountForm(forms.ModelForm):
#     valid_from =  forms.DateField(
#     widget=forms.DateInput(format='%d-%m-%Y %H:%M:%S',attrs={'placeholder':"DD-MM-YY HH:MM:SS"}),
# )
#     valid_to = forms.DateField(
#     widget=forms.DateInput(format='%d-%m-%Y %H:%M:%S',attrs={'placeholder':"DD-MM-YY HH:MM:SS"}),
# )
    class Meta:
        model = Coupon
        fields = ['code','discount','active','valid_from','valid_to']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for myField in self.fields:
    #         self.fields[myField].widget.attrs['class'] = 'form-control'
