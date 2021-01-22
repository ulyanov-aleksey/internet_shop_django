from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.decorators.cache import cache_page

from mainapp import views as mainviews

app_name = 'mainapp'

urlpatterns = [
    path('', mainviews.products, name='index'),
    path('<int:pk>/', cache_page(3600)(mainviews.products), name='category'),
    path('<int:pk>/<page>/', mainviews.products, name='page'),
    path('product/<int:pk>/', mainviews.product, name='product')

]

