from django.urls import path, re_path
from . import views

urlpatterns = [

    path('register/', views.register, name='register'),
    path('register_exist/', views.register_exist, name='register_exist'),  # 判断 用户名是否存在
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('favor/', views.favor, name="favor"),
    path('address/',views.editaddress,name='address'),
    path('getaddress/', views.getaddress),
    path('editpwd/',views.editpassword,name='eidtpwd'),
    path('editpwd1/', views.editpwdUnlogin,name='editpwd1'),
    path('personalinfo/',views.personalinfo,name='personalinfo'),
    path('paydeposit/', views.payDeposit, name='paydeposit'),
    path('refunddeposit/', views.refundDeposit, name='refunddeposit'),
    path('charge/', views.charge, name='charge'),

]

app_name = 'user'