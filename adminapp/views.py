from django.contrib.auth.decorators import user_passes_test
from django.db import connection
from django.db.models import F
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductsCategores, Products


# пользователи
# @user_passes_test(lambda u: u.is_superuser)
# def user_create(request):
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin:users'))
#
#     else:
#         user_form = ShopUserRegisterForm()
#
#     content = {
#         'update_form': user_form
#     }
#     return render(request, 'adminapp/user_update.html', content)


# контроллер CBV
class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('adminapp:users')
    form_class = ShopUserRegisterForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователь/создание'
        return context


# исключаем доступ к админке не админа, даже по адресу /admin/users/read
# @user_passes_test(lambda u: u.is_superuser)
# # read
# def users(request):
#     users_list = ShopUser.objects.all().order_by('-is_active')
#     content = {
#         'objects': users_list
#     }
#     return render(request, 'adminapp/users.html', content)


# контроллер CBV
class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    # paginate_by = 3   # пагинация в CBV

    # декоратор для проверки на суперпользователя
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/пользователи'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def user_update(request, pk):
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('adminapp:user_update', args=[edit_user.pk]))
#     else:
#         edit_form = ShopUserAdminEditForm(instance=edit_user)
#
#     content = {
#         'update_form': edit_form
#     }
#     return render(request, 'adminapp/user_update.html', content)


# контроллер CBV
class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('adminapp:users')
    form_class = ShopUserAdminEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/редактирование'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def user_delete(request, pk):
#     user_item = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         if user_item.is_active:
#             user_item.is_active = False
#         else:
#             user_item.is_active = True
#         user_item.save()
#         return HttpResponseRedirect(reverse('admin:users'))
#
#     content = {
#         'user_to_delete': user_item
#     }
#     return render(request, 'adminapp/user_delete.html', content)


# контроллер CBV
class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('adminapp:users')

    # переопределяем метод удаления, используем is_active
    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/удаление'
        return context


# категории
# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     if request.method == 'POST':
#         category_form = ProductCategoryEditForm(request.POST, request.FILES)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('admin:categories'))
#
#     else:
#         category_form = ProductCategoryEditForm()
#
#     content = {
#         'update_form': category_form
#     }
#     return render(request, 'adminapp/categories_update.html', content)


# контроллер CBV
class ProductCategoryCreateView(CreateView):
    model = ProductsCategores
    template_name = 'adminapp/categories_update.html'
    success_url = reverse_lazy('adminapp:categories')
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/создание'
        return context


# read
# @user_passes_test(lambda u: u.is_superuser)
# def categories(request):
#     categories_list = ProductsCategores.objects.all().order_by('-is_active')
#     content = {
#         'objects': categories_list
#     }
#     return render(request, 'adminapp/categories.html', content)


# контроллер CBV
class ProductCategoryListView(ListView):
    model = ProductsCategores
    template_name = 'adminapp/categories.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'админка/категории'
        # print(context['object_list'])
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):

#     edit_category = get_object_or_404(ProductsCategores, pk=pk)
#     if request.method == 'POST':
#         edit_form = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('adminapp:category_update', args=[edit_category.pk]))
#     else:
#         edit_form = ProductCategoryEditForm(instance=edit_category)
#
#     content = {
#         'update_form': edit_form
#     }
#     return render(request, 'adminapp/categories_update.html', content)


# контроллер CBV
class ProductCategoryUpdateView(UpdateView):
    model = ProductsCategores
    template_name = 'adminapp/categories_update.html'
    success_url = reverse_lazy('adminapp:categories')
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    # переопределяем метод контента класса, определяем title
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категория/редактирование'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                # db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)


# Сигнал для установки is_active для Продукта категории в зависимости от значения в Категории
# def db_profile_by_type(prefix, type, queries):
#     update_queries = list(filter(lambda x: type in x['sql'], queries))
#     print(f'db_profile {type} for {prefix}:')
#     [print(query['sql']) for query in update_queries]
#
#
# @receiver(pre_save, sender=ProductsCategores)
# def product_is_active_update_productcategory_save(sender, instance, **kwargs):
#     if instance.pk:
#         if instance.is_active:
#             instance.product_set.update(is_active=True)
#         else:
#             instance.product_set.update(is_active=False)
#
#         db_profile_by_type(sender, 'UPDATE', connection.queries)


# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request, pk):
#     category_item = get_object_or_404(ProductsCategores, pk=pk)
#
#     if request.method == 'POST':
#         if category_item.is_active:
#             category_item.is_active = False
#         else:
#             category_item.is_active = True
#         category_item.save()
#         return HttpResponseRedirect(reverse('admin:categories'))
#
#     content = {
#         'category_to_delete': category_item
#     }
#     return render(request, 'adminapp/categories_delete.html', content)


# контроллер CBV
class ProductCategoryDeleteView(DeleteView):
    model = ProductsCategores
    template_name = 'adminapp/categories_delete.html'
    success_url = reverse_lazy('adminapp:categories')

    # переопределяем метод удаления, используем is_active
    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    # декоратор для проверки на суперпользователя
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категория/удаление'
        return context


# товары
# @user_passes_test(lambda u: u.is_superuser)
# def product_create(request, pk):
#     category_item = get_object_or_404(ProductsCategores, pk=pk)
#     # print(category_item)
#     if request.method == 'POST':
#         update_form = ProductEditForm(request.POST, request.FILES)
#         if update_form.is_valid():
#             update_form.save()
#             return HttpResponseRedirect(reverse('admin:products', args=[pk]))
#     else:
#         update_form = ProductEditForm()
#     content = {
#         'update_form': update_form,
#         'category': category_item
#     }
#     return render(request, 'adminapp/product_update.html', content)


class ProductCreateViev(CreateView):
    model = Products
    template_name = 'adminapp/product_update.html'
    form_class = ProductEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        category_pk = self.kwargs['pk']
        category_item = get_object_or_404(ProductsCategores, pk=category_pk)
        context['title'] = 'продукт/создание'
        context['category'] = category_item
        return context

    # переопределяем success_url т.к. дополнительно нужна категория рк
    def get_success_url(self):
        category_pk = self.kwargs['pk']
        success_url = reverse('adminapp:products', args=[category_pk])
        return success_url


# read
# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk):
#     title = 'админка/продукт'
#     category_item = get_object_or_404(ProductsCategores, pk=pk)
#     products_list = Products.objects.filter(category=category_item)
#
#     content = {
#         'title': title,
#         'objects': products_list,
#         'category': category_item
#     }
#     return render(request, 'adminapp/products.html', content)


class ProductListView(ListView):
    model = Products
    template_name = 'adminapp/products.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    # переопрелеляем метод queryset
    def get_queryset(self):
        queryset = super().get_queryset()  # вытащили queryset из Products
        category_pk = self.kwargs['pk']
        return queryset.filter(category__pk=category_pk)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        category_pk = self.kwargs['pk']
        category_item = get_object_or_404(ProductsCategores, pk=category_pk)
        context['title'] = 'админка/продукт'
        context['category'] = category_item
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     product_item = get_object_or_404(Products, pk=pk)
#     content = {
#         'object': product_item,
#     }
#     return render(request, 'adminapp/product_read.html', content)


# контроллер CBV описание
class ProductDetailView(DetailView):
    model = Products
    template_name = 'adminapp/product_read.html'

    # декоратор для проверки на суперпользователя
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(context)
        context['title'] = 'продукт/свойства'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def product_update(request, pk):
#     product_item = get_object_or_404(Products, pk=pk)
#
#     if request.method == 'POST':
#         update_form = ProductEditForm(request.POST, request.FILES, instance=product_item)
#         if update_form.is_valid():
#             update_form.save()
#             return HttpResponseRedirect(reverse('adminapp:products', args=[pk]))
#     else:
#         update_form = ProductEditForm(instance=product_item)
#     content = {
#         'update_form': update_form,
#         'category': product_item.category
#     }
#     return render(request, 'adminapp/product_update.html', content)


class ProductUpdateView(UpdateView):
    model = Products
    template_name = 'adminapp/product_update.html'
    form_class = ProductEditForm

    # success_url = reverse_lazy('adminapp:product_update')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        product_pk = self.kwargs['pk']
        # print(product_pk,'product_pk')
        product_item = get_object_or_404(Products, pk=product_pk)
        # print(product_item.category.pk, 'category_pk')
        context['title'] = 'продукт/редактирование'
        context['category'] = product_item
        return context

    # переопределяем success_url т.к. дополнительно нужна категория рк
    def get_success_url(self):
        category_pk = self.kwargs['pk']
        print(category_pk)
        success_url = reverse('adminapp:product_read', args=[category_pk])
        return success_url


# class ProductUpdateView(UpdateView):
#     model = Products
#     template_name = 'adminapp/product_update.html'
#     form_class = ProductEditForm
#
#     # success_url = reverse_lazy('adminapp:product_update')
#
#     @method_decorator(user_passes_test(lambda u: u.is_superuser))
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         category_pk = self.kwargs['pk']
#         category_item = get_object_or_404(Products, pk=category_pk)
#         context['title'] = 'продукт/редактирование'
#         context['category'] = category_item
#         return context
#
#     # переопределяем success_url т.к. дополнительно нужна категория рк
#     def get_success_url(self):
#         category_pk = self.kwargs['pk']
#         success_url = reverse('adminapp:product_read', args=[category_pk])
#         return success_url


# @user_passes_test(lambda u: u.is_superuser)
# def product_delete(request, pk):
#     title = 'продукты/удаление'
#
#     product = get_object_or_404(Products, pk=pk)
#
#     if request.method == 'POST':
#         if product.is_active:
#             product.is_active = False
#         else:
#             product.is_active = True
#         product.save()
#         return HttpResponseRedirect(reverse('adminapp:products', args=[product.category_id]))
#
#     content = {
#         'title': title,
#         'product_to_delete': product
#     }
#     return render(request, 'adminapp/product_delete.html', content)

class ProductDeleteView(DeleteView):
    model = Products
    template_name = 'adminapp/product_delete.html'

    # success_url = reverse_lazy('adminapp:products')

    # декоратор для проверки на суперпользователя
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'товар/удаление'
        return context

    # переопределяем метод удаления, используем is_active
    def delete(self, request, *args, **kwargs):
        object = self.get_object()
        if object.is_active:
            object.is_active = False
        else:
            object.is_active = True
        object.save()

        return HttpResponseRedirect(reverse('adminapp:products', args=[object.category_id]))

# Create your views here.
