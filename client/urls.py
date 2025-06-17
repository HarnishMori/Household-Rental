from django.contrib import admin
from django.urls import path,include
from client import views

urlpatterns = [
    path("", views.index, name='index'),
    path("register/", views.register, name='register'),
    path("login/", views.loginview,name='login'),
    path("logout/", views.logoutview, name='logout'),
    path("ItemForm/", views.itemform, name='itemform'),
    path("confirmorder/", views.checkout, name='cnforder'),
    path("ordercnf/", views.ordercnf, name='ordercnf'),
]