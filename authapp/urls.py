from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from authapp import views as authviews

app_name = 'authapp'

urlpatterns = [
    path('login/', authviews.login, name='login'),
    path('logout/', authviews.logout, name='loguot'),
    path('register/', authviews.register, name='register'),
    path('edit/', authviews.edit, name='edit'),
    path('verify/<email>/<activation_key>/', authviews.verify, name='verify')
]

