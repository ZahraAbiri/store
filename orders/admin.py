# from django.contrib import admin
#
# from .models import Orders
# admin.site.register(Orders)

from django.contrib import admin
from .models import Order, OrderItem, Coupon


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	raw_id_fields = ('product',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'updated', 'paid','sent_status')
	list_filter = ('paid',)
	inlines = (OrderItemInline,)


admin.site.register(Coupon)
