import json
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import BaseCommand

from authapp.models import ShopUser
from mainapp.models import ProductsCategores, Products

JSON_PATH = os.path.join(settings.BASE_DIR, 'mainapp/json')

def load_json_data (file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json')) as json_file:
        return json.load(json_file)


class Command(BaseCommand):

    def handle(self, *args, **options):
        categores = load_json_data('categores')
        ProductsCategores.objects.all().delete()
        for category in categores:
            ProductsCategores.objects.create(**category)

        products = load_json_data('products')
        Products.objects.all().delete()
        for product in products:
            cat_name = product['category']
            _cat = ProductsCategores.objects.get(name=cat_name)
            product['category'] = _cat
            Products.objects.create(**product)

        ShopUser.objects.create_superuser('django', 'email=None', 'geekbrains', age=45)   ## Эту строку оставляем когда пересоздаем базу!!!!