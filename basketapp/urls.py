from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from basketapp import views as basketviews

app_name = 'basketapp'

urlpatterns = [
    path('', basketviews.basket, name='view'),
    path('add/<int:pk>/', basketviews.add, name='add'),
    path('remove/<int:pk>/', basketviews.remove, name='remove'),
    path('edit/<int:pk>/<int:quantity>/', basketviews.basket_edit, name='edit'),
]
