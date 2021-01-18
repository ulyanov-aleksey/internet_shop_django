from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from ordersapp import views as ordersappviews

app_name = 'ordersapp'

urlpatterns = [
    path('', ordersappviews.OrderListView.as_view(), name='orders_list'),
    path('create/', ordersappviews.OrderCreateView.as_view(), name='order_create'),
    path('read/<int:pk>/', ordersappviews.OrderDetailView.as_view(), name='order_read'),
    path('edit/<int:pk>/', ordersappviews.OrderUpdateView.as_view(), name='order_update'),
    path('delete/<int:pk>/', ordersappviews.OrderDeleteView.as_view(), name='order_delete'),
    path('complete/<int:pk>/', ordersappviews.order_forming_complete, name='order_forming_complete'),
    re_path(r'^product/(?P<pk>\d+)/price/$', ordersappviews.get_product_price)
]