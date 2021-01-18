import os
import urllib.request
from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django import forms
from django.conf import settings
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile, ShopUser


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'photo_200_orig')),
                                                access_token=response['access_token'],
                                                v='5.92')),
                          None
                          ))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]  # response - словарь в котором содержаться данные пользователя
    if data['sex']:
        user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE

    if data['about']:
        user.shopuserprofile.aboutMe = data['about']

    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

        age = timezone.now().date().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2') and forms.ValidationError(
                'Вам меньше 18. Доступ закрыт.')
        user.age = age
    # user.avatar =
    # if age > 100:
    #     user.delete()
    #     raise AuthForbidden('social_core.backends.vk.VKOAuth2') and forms.ValidationError('Проверьте данные возраста.')

    if data['photo_200_orig']:
        # метод вытягивает фото и ВК и сохраняет его в MEDIA_ROOT ...с user.pk.jpg
        urllib.request.urlretrieve(data['photo_200_orig'],
                                   os.path.join(settings.MEDIA_ROOT, 'users_avatar', f'{user.pk}.jpg')
                                   )
        # добавляем фото в поле upload_to='users_avatar' у ShopUser с user.pk.jpg
        user.avatar = os.path.join('users_avatar', f'{user.pk}.jpg')

        # print(user.avatar)
        # user.avatar.delete()
    user.save()
