from django.shortcuts import render
from django import views
from django.contrib import admin
from django.urls import include,path
from .import views

urlpatterns = [
    path('',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('index/',views.index,name='index'),
    path('details/<int:product_id>/',views.details,name='details'),
    path('mycart/<int:product_id>/',views.mycart,name='mycart'),
    path('delete/<int:cart_id>/',views.delete,name='delete'),
    path('search/', views.search, name='search'),
    path('logout/', views.user_logout, name='logout'),
]


