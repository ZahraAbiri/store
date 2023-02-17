from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.HomeView.as_view(), name='products'),
    path('category/<slug:category_slug>/', views.HomeView.as_view(), name='category_filter'),
    # path('bucket/', include(bucket_urls)),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),

    path('productlist/list/', views.productList, name='productlist'),
    path('productcreate/create/', views.productCreate, name='productcreate'),
    path('productupdate/<int:id>/', views.update_view, name='productupdate'),
    path('productdelete/<int:id>/', views.delete_view, name='productdelete'),

    path('categorylist/list/', views.categoryList, name='categorylist'),
    path('categorycreate/create/', views.categoryCreate, name='categorycreate'),
    path('categoryupdate/<int:id>/', views.update_category, name='categoryupdate'),
    path('categorydelete/<int:id>/', views.delete_category, name='categorydelete'),

    path('discountlist/list/', views.discountList, name='discountlist'),
    path('discountcreate/create/', views.discountCreate, name='discountcreate'),
    path('discountupdate/<int:id>/', views.update_discount, name='discountupdate'),
    path('discountdelete/<int:id>/', views.delete_discount, name='discountdelete'),


]


