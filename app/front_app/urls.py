from django.contrib import admin
from django.urls import path, include
from app.views import *
from app.front_app import views

urlpatterns = [
    path('oops/', views.viewOops, name='oops'),

    path('auth/', views.viewAuth, name='auth'),
    path('registration/', views.viewRegistration, name='registration'),
    path('profile/', views.viewProfile, name='profile'),
    path('profile/<int:id>/', views.viewProfile, name='profileId'),
    path('payment/', views.viewPayment, name='payment'),
    path('withdraw/', views.viewWithdraw, name='withdraw'),
    path('operations/', views.viewOperations, name='operations'),
    path('operations/<int:id>/', views.viewOperationsDetail, name='operationsDetail'),
    path('analytic/', views.viewAnalytic, name='analytic'),


    path('enterprise/<int:id>/', views.viewEnterprise, name='enterprise'),
    path('tradeHistory/<int:id>/', views.viewTradeHistory, name='tradeHistory'),
    path('analytic/<int:id>/', views.viewAnalytic, name='Manalytic'),
    path('trade/<int:id>/', views.viewTrade, name='trade'),
    path('securitiesTrade/<int:id>/<ticker>/', views.viewSecuritiesTrade, name='securitiesTrade'),

    path('employee/<int:id>/', views.viewEmployee, name='employee'),


    path('', views.viewHome, name='/')
] 
