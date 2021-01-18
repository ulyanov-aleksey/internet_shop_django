import json
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import BaseCommand

from authapp.models import ShopUser, ShopUserProfile
from mainapp.models import ProductsCategores, Products

JSON_PATH = os.path.join(settings.BASE_DIR, 'mainapp/json')


def load_json_data(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json')) as json_file:
        return json.load(json_file)


class Command(BaseCommand):

    def handle(self, *args, **options):
        users = ShopUser.objects.all()
        for user in users:
            users_profile = ShopUserProfile.objects.create(user=user)
            users_profile.save()
