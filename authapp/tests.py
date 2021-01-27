from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command

from authapp.models import ShopUser


class TestAuthUserTestCase(TestCase):

    def setUp(self):
        call_command('flush', '--noinput')
        self.client = Client()

        # создается супер-пользователь
        self.superuser = ShopUser.objects.create_superuser('django', 'django@gb.local', 'geekbrains')

        # создаются пользователи
        self.user = ShopUser.objects.create_user('test_1', 'test_1@gb.local', 'geekbrains')
        self.user_with_fn = ShopUser.objects.create_user('test_2', 'test_2@gb.local', 'geekbrains', first_name='Test_2')

    def test_user_login(self):
        # главная без логина
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context['title'], 'Главная')
        self.assertNotContains(response, 'Пользователь', status_code=200)
        # self.assertNotIn('Пользователь', response.content.decode())

        # данные пользователя
        self.client.login(username='django', password='geekbrains')

        # логинимся
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.superuser)

        # главная после логина
        response = self.client.get('/')
        self.assertContains(response, 'Пользователь', status_code=200)
        self.assertEqual(response.context['user'], self.superuser)
        # self.assertIn('Пользователь', response.content.decode())

    def test_user_logout(self):
        self.client.login(username='django', password='geekbrains')

        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)

        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 302)

    # функция для завершения теста(очистка временных данных)
    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')
