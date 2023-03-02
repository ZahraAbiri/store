from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('verify/', views.UserRegisterVerifyCodeView.as_view(), name='verify_code'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('loginapi/', views.loginView.as_view(), name='user_login_api'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),

    path('addresslist/list/', views.addressList, name='addresslist'),
    path('addressListManagement/list/', views.addressListManagement, name='addressListManagement'),
    path('addresscreate/create/', views.addressCreate, name='addresscreate'),
    path('addressupdate/<int:id>/', views.update_address, name='addressupdate'),
    path('addressdelete/<int:id>/', views.delete_address, name='addressdelete'),
    path('profileUpdate/', views.profileUpdate, name='profileUpdate'),
    path('nazer_panel/', views.nazer_panel, name='nazer_panel'),
    path('usercreate/', views.Operator_user_create, name='usercreate'),
    path('userlist/', views.operator_user_List, name='userlist'),
    path('userupdate/<int:id>/', views.update_Operator_user_, name='userupdate'),
    path('userdelete/<int:id>/', views.delete_user_operator, name='userdelete'),
    path('customer/addAddress', views.customerAddAddress, name='cusAdd'),
]
