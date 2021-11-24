from django.contrib import admin
from django.urls import path

from ordersapp import views as ordersapp
from mainapp import views as mainapp
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include

app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.OrderListView.as_view(), name='list'),
    path('read/<pk>/', ordersapp.OrderDetailView.as_view(), name='read'),
    path('create/', ordersapp.OrderCreateView.as_view(), name='create'),
    path('update/<pk>/', ordersapp.OrderUpdateView.as_view(), name='update'),
    path('delete/<pk>/', ordersapp.OrderDeleteView.as_view(), name='delete'),
    path('cancel/forming/<pk>/', ordersapp.order_forming_complete, name='forming_cancel'),
]