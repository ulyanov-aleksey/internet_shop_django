from django.conf import settings
from django.db import models

from mainapp.models import Products


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(auto_now_add=True, verbose_name='время')

    # создаем метод для вычисления общей стоимости товара в зависимости от количества
    # берем продукт из basket и уьножаем на иго количество quantity
    @property
    def product_cost(self):
        return self.product.price * self.quantity

    # вытаскиваем общее колическто из корзины пользователя
    @property
    def total_quantity(self):
        # фильтр карзины для одного пользователя
        _items = Basket.objects.filter(user=self.user)
        # суммируем общее кол товаров в данной корзине
        _total_quantity = sum(list(map(lambda x: x.quantity, _items)))
        return _total_quantity

    # аналогично метод для общей стоимости
    @property
    def total_cost(self):
        # фильтр карзины для одного пользователя
        _items = Basket.objects.filter(user=self.user)
        # суммируем общее счтоимость товаров в данной корзине
        _total_cost = sum(list(map(lambda x: x.product_cost, _items)))
        return _total_cost

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)

# Create your models here.
