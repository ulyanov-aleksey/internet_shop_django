import json
import os
import random

from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
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


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductsCategores, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductsCategores, pk=pk)


#####
def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Products.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Products.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Products, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Products, pk=pk)


def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Products.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Products.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Products.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
                'price')
            cache.set(key, products)
        return products
    else:
        return Products.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


####
def get_hot_product():
    products = get_products()
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Products.objects.filter(category__pk=hot_product.category.pk).exclude(pk=hot_product.pk)[:3]
    return same_products


def main(request):
    title = 'Главная'
    products = get_products()[:3]
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


# Кеширование контактов
# def contact(request):
#    title = 'о нас'
#    if settings.LOW_CACHE:
#        key = f'locations'
#        locations = cache.get(key)
#        if locations is None:
#            locations = load_from_json('contact__locations')
#            cache.set(key, locations)
#    else:
#        locations = load_from_json('contact__locations')


def products(request, pk=None, page=1):
    print(pk)
    title = 'продукты'
    links_prodMenu = get_links_menu()

    if pk is not None:
        if pk == 0:
            products_list = get_products_orederd_by_price()
            category = {'name': 'все', 'pk': 0}
        else:
            category = get_category(pk)
            # products_list = get_products_in_category_orederd_by_price(pk)
            products_list = Products.objects.filter(Q(category_pk=1) | Q(category_pk=2))   # использование Q-обьектов

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
        'links_menu': get_links_menu(),
        'product': get_product(pk),
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
