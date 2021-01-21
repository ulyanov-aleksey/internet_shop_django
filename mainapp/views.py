import json
import os
import random

from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.core.cache import cache

from basketapp.models import Basket
from mainapp.models import Products, ProductsCategores


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductsCategores.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductsCategores.objects.filter(is_active=True)


def get_hot_product():
    products = Products.objects.all()
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Products.objects.filter(category__pk=hot_product.category.pk).exclude(pk=hot_product.pk)[:3]
    return same_products


def main(request):
    title = 'Главная'
    products = Products.objects.all()[:3]
    content = {
        'title': title,
        'products': products,
    }
    return render(request, 'mainapp/index.html', content)


def contactes(request):
    location = []
    file_path = os.path.join(settings.BASE_DIR, 'our_contacts.json')
    with open(file_path, encoding="utf-8") as file_contacts:
        location = json.load(file_contacts)
    content = {
        'title': 'контакты',
        'location': location,
    }
    return render(request, 'mainapp/contact.html', content)


def products(request, pk=None, page=1):
    print(pk)
    title = 'продукты'
    links_prodMenu = get_links_menu()

    if pk is not None:
        if pk == 0:
            products_list = Products.objects.all()
            category = {'name': 'все', 'pk': 0}
        else:
            category = get_object_or_404(ProductsCategores, pk=pk)
            products_list = Products.objects.filter(category__pk=category.pk)

        paginator = Paginator(products_list, 2)
        # обработка исключений
        try:
            product_paginator = paginator.page(page)
        except PageNotAnInteger:
            product_paginator = paginator.page(1)  # Если польз ввел некоректный номер страницы, вывод первой стр
        except EmptyPage:
            product_paginator = paginator.page(
                paginator.num_pages)  # Если польз ввел номер страницы больше чем есть, вывод последней стр

        content = {
            'title': title,
            'links_prodMenu': links_prodMenu,
            'products': product_paginator,
            'category': category,
        }
        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': title,
        'links_prodMenu': links_prodMenu,
        'same_products': same_products,
        'hot_product': hot_product,
    }
    return render(request, 'mainapp/products.html', content)


def product(request, pk):
    title = 'продукты'
    content = {
        'title': title,
        'links_menu': ProductsCategores.objects.all(),
        'product': get_object_or_404(Products, pk=pk),
    }
    return render(request, 'mainapp/product.html', content)


def products_All(request):
    links_prodMenu = [
        {'href': 'products_All'},
        {'href': 'products_Home'},
        {'href': 'products_Office'},
        {'href': 'products_Modern'},
        {'href': 'products_Classic'}
    ]
    content = {
        'title': 'продукты',
        'links_prodMenu': links_prodMenu
    }
    return render(request, 'mainapp/products.html', content)


def products_Home(request):
    links_prodMenu = [
        {'href': 'products_All'},
        {'href': 'products_Home'},
        {'href': 'products_Office'},
        {'href': 'products_Modern'},
        {'href': 'products_Classic'}
    ]
    content = {
        'title': 'продукты',
        'links_prodMenu': links_prodMenu
    }
    return render(request, 'mainapp/products.html', content)


def products_Office(request):
    links_prodMenu = [
        {'href': 'products_All'},
        {'href': 'products_Home'},
        {'href': 'products_Office'},
        {'href': 'products_Modern'},
        {'href': 'products_Classic'}
    ]
    content = {
        'title': 'продукты',
        'links_prodMenu': links_prodMenu
    }
    return render(request, 'mainapp/products.html', content)


def products_Modern(request):
    links_prodMenu = [
        {'href': 'products_All'},
        {'href': 'products_Home'},
        {'href': 'products_Office'},
        {'href': 'products_Modern'},
        {'href': 'products_Classic'}
    ]
    content = {
        'title': 'продукты',
        'links_prodMenu': links_prodMenu
    }
    return render(request, 'mainapp/products.html', content)


def products_Classic(request):
    links_prodMenu = [
        {'href': 'products_All'},
        {'href': 'products_Home'},
        {'href': 'products_Office'},
        {'href': 'products_Modern'},
        {'href': 'products_Classic'}
    ]
    content = {
        'title': 'продукты',
        'links_prodMenu': links_prodMenu
    }
    return render(request, 'mainapp/products.html', content)
# Create your views here.
