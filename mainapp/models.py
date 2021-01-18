from django.db import models


class ProductsCategores(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='имя')
    description = models.TextField(verbose_name='описание')
    is_active = models.BooleanField(default=True, verbose_name='категория активна')

    def __str__(self):
        return self.name


class Products(models.Model):
    category = models.ForeignKey(ProductsCategores, on_delete=models.CASCADE, verbose_name='категория')
    name = models.CharField(max_length=128, verbose_name='наименование')
    image = models.ImageField(upload_to='products_images', blank=True, verbose_name='изображение')
    short_description = models.CharField(max_length=120, verbose_name='краткое описание продукта')
    description = models.TextField(blank=True, verbose_name='полное описание продукта')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='цена')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='количество на складе')
    is_active = models.BooleanField(default=True, verbose_name='продукт активен')

    def __str__(self):
        return f'{self.name} ({self.category.name})'

    @staticmethod
    def get_items():
        return Products.objects.filter(is_active=True).order_by('category', 'name')

# Create your models here.
