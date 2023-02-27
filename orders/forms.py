from ckeditor.fields import RichTextField
from django import forms

from orders.models import OrderItem
from products.models import Category


class CartAddForm(forms.Form):
	quantity = forms.IntegerField(min_value=1, max_value=9)


class CouponApplyForm(forms.Form):
	code = forms.CharField()

class orderItemForm(forms.ModelForm):
	class Meta:
		model = OrderItem
		fields='__all__'

