from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from adminapp import views as adminviews

app_name = 'adminapp'

urlpatterns = [
    # path('users/create', adminviews.user_create, name='user_create'),
    path('users/create', adminviews.UserCreateView.as_view(), name='user_create'),
    # path('users/read', adminviews.users, name='users'),
    path('users/read', adminviews.UsersListView.as_view(), name='users'),      #патерн для контроллера CBV
    # path('users/update/<pk>/', adminviews.user_update, name='user_update'),
    path('users/update/<pk>/', adminviews.UserUpdateView.as_view(), name='user_update'),
    # path('users/delete/<pk>/', adminviews.user_delete, name='user_delete'),
    path('users/delete/<pk>/', adminviews.UserDeleteView.as_view(), name='user_delete'),

    # path('categories/create', adminviews.category_create, name='category_create'),
    path('categories/create', adminviews.ProductCategoryCreateView.as_view(), name='category_create'),
    # path('categories/read', adminviews.categories, name='categories'),
    path('categories/read', adminviews.ProductCategoryListView.as_view(), name='categories'),
    # path('categories/update/<pk>/', adminviews.category_update, name='category_update'),
    path('categories/update/<pk>/', adminviews.ProductCategoryUpdateView.as_view(), name='category_update'),
    # path('categories/delete/<pk>/', adminviews.category_delete, name='category_delete'),
    path('categories/delete/<pk>/', adminviews.ProductCategoryDeleteView.as_view(), name='category_delete'),

    # path('products/create/category/<pk>', adminviews.product_create, name='product_create'),
    path('products/create/category/<pk>', adminviews.ProductCreateViev.as_view(), name='product_create'),
    # path('products/read/category/<pk>', adminviews.products, name='products'),
    path('products/read/category/<pk>', adminviews.ProductListView.as_view(), name='products'),
    # path('products/read/<pk>', adminviews.product_read, name='product_read'),
    path('products/read/<pk>', adminviews.ProductDetailView.as_view(), name='product_read'),
    # path('products/update/<pk>/', adminviews.product_update, name='product_update'),
    path('products/update/<pk>/', adminviews.ProductUpdateView.as_view(), name='product_update'),
    # path('products/delete/<pk>/', adminviews.product_delete, name='product_delete'),
    path('products/delete/<pk>/', adminviews.ProductDeleteView.as_view(), name='product_delete'),



]

