from django.test import TestCase

from django.test import TestCase
from django.test.client import Client
from mainapp.models import Products, ProductsCategores
from django.core.management import call_command


# Create your tests here.

class TestMainappSmoke(TestCase):

    def setUp(self):
        call_command('flush', '--noinput')
        test_category = ProductsCategores.objects.create(name='Тест')  # в пустой бд(для теста) создаем категорию
        Products.objects.create(  # создаем продукт в этой категории
            category=test_category,
            name='Product_test_1'
        )
        Products.objects.create(
            category=test_category,
            name='Product_test_2'
        )

        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('/')  # какой url тестируем
        self.assertEqual(response.status_code, 200)  # проверка на код 200(ОК)

        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

    def test_products_pages(self):
        for category in ProductsCategores.objects.all():
            response = self.client.get(f'/products/category/{category.pk}/')
            self.assertEqual(response.status_code, 200)

        for product in Products.objects.all():
            response = self.client.get(f'/products/product/{product.pk}/')
            self.assertEqual(response.status_code, 200)

        # функция для завершения теста(очистка временных данных)
    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')


# тестирование дублированием бд
    # class TestMainappSmoke(TestCase):
    #     def setUp(self):                    # В этом методе указываем какими данными заполнить тестируемую бд
    #         call_command('flush', '--noinput')
    #         call_command('loaddata', 'test_db.json')
    #         self.client = Client()
    #
    #     def test_mainapp_urls(self):
    #         response = self.client.get('')   # какой url тестируем
    #         self.assertEqual(response.status_code, 200)

    # response = self.client.get('/contacts/')
    # self.assertEqual(response.status_code, 200)
    #
    # response = self.client.get('/products/')
    # self.assertEqual(response.status_code, 200)
    #
    # response = self.client.get('/products/category/0/')
    # self.assertEqual(response.status_code, 200)
    #
    # for category in ProductsCategores.objects.all():
    #     response = self.client.get(f'/products/category/{category.pk}/')
    #     self.assertEqual(response.status_code, 200)
    #
    # for product in Products.objects.all():
    #     response = self.client.get(f'/products/product/{product.pk}/')
    #     self.assertEqual(response.status_code, 200)

    # def tearDown(self):  # функция для завершения теста(очистка временных данных)
    #     call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')
