
from django.urls import path

from . import views

app_name = 'orders'
urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('detail/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', views.CartAddView.as_view(), name='cart_add'),
    path('cart/remove/<int:product_id>/', views.CartRemoveView.as_view(), name='cart_remove'),
    path('pay/<int:order_id>/', views.OrderPayView.as_view(), name='order_pay'),
    path('verify/', views.OrderVerifyView.as_view(), name='order_verify'),
    path('apply/<int:order_id>/', views.CouponApplyView.as_view(), name='apply_coupon'),
    path('', views.OrderView.as_view(), name='OrderView'),  # endpoint
    path('all/', views.showAllOrders),
    path('allOrderItem/', views.showAllOrderItems),
    path('orderView/<int:pk>/', views.show),
    path('orderItemView/<int:pk>/', views.showOrderItemView),
    path('orderHistoryList/history/', views.orderHistoryList,name='orderHistoryList'),
    path('orderStatusList/status/', views.orderStatusList,name='orderHistoryStatusList'),
    path('order_List/list/', views.order_List,name='order_List'),
    path('orderItemcreate/', views.orderItemcreate,name='orderItemcreate'),
    path('orderItemDelete/<int:id>/', views.orderItemDelete,name='orderItemDelete'),
    path('orderItemUpdate/<int:id>/', views.orderItemUpdate,name='orderItemUpdate'),
    # path('getAllProduct/test/', views.getAllProduct,name='getAllProduct'),
]
