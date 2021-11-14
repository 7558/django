from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from authapp.forms import ShopUserRegisterForm
from adminapp.forms import ShopUserAdminEditForm
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from adminapp.forms import ProductEditForm


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     title = 'админка/пользователи'
#
#     # user_list = ShopUser.objects.all().order_by('-is_active')
#
#     context = {
#         'objects': ShopUser.objects.all().order_by('-is_active'),
#         'title': title,
#         # 'objects': user_list
#     }
#
#     return render(request, 'adminapp/users.html', context)

class AccessMixin:

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserListView(AccessMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'пользователи/создание'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:users'))
    else:
        user_form = ShopUserRegisterForm()

    context = {
        'title': title,
        'update_form': user_form
    }

    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'пользователи/редактирование'

    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('adminapp:user_update', args=[edit_user.pk]))
    else:
        edit_form = ShopUserAdminEditForm(instance=edit_user)

    context = {
        'title': title,
        'update_form': edit_form
    }

    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = 'пользователи/удаление'

    current_user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        if current_user.is_active:
            current_user.is_active = False
        else:
            current_user.is_active = True
        current_user.save()
        return HttpResponseRedirect(reverse('adminapp:user_list'))

    context = {
        'title': title,
        'user_to_delete': current_user
    }

    return render(request, 'adminapp/user_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'админка/категории'

    context = {
        'objects': ProductCategory.objects.all().order_by('-is_active'),
        # 'objects': user_list
    }

    return render(request, 'adminapp/categories.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    context = {

    }

    return render(request, 'adminapp/users.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    context = {

    }

    return render(request, 'adminapp/users.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    context = {

    }

    return render(request, 'adminapp/users.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk):
#     title = 'админка/продукт'
#
#     category = get_object_or_404(ProductCategory, pk=pk)
#     product_list = Product.objects.filter(category__pk=pk).order_by('name')
#
#     context = {
#         'title': title,
#         'category': category,
#         'objects': product_list,
#     }
#
#     return render(request, 'adminapp/products.html', context)

class ProductListView(AccessMixin, ListView):
    model = Product,
    template_name = 'adminapp/products.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['category'] = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        return context_data

    def get_queryset(self):
        return Product.objects.filter(category__pk=self.kwargs.get('pk'))



# @user_passes_test(lambda u: u.is_superuser)
# def product_detail(request, pk):
#     title = 'продукты/подробнее'
#     product = get_object_or_404(Product, pk=pk)
#     context = {
#         'title': title,
#         'object': product,
#     }
#
#     return render(request, 'adminapp/product_read.html', context)

class ProductDetailView(AccessMixin, DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'


# @user_passes_test(lambda u: u.is_superuser)
# def product_create(request, pk):
#     title = 'продукты/создание'
#     category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         product_form = ProductEditForm(request.POST, request.FILES)
#         if product_form.is_valid():
#             product_form.save()
#             return HttpResponseRedirect(reverse('adminapp:products', args=[pk]))
#         else:
#             product_form = ProductEditForm(initial={'category': category})
#     context = {
#         'title': title,
#         'update_form': product_form,
#         'category': category,
#     }
#
#     return render(request, 'adminapp/product_update.html', context)

class ProductCreateView(AccessMixin, CreateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    # form_class = ProductEditForm
    fields = '__all__'
    # success_url = reverse_lazy('adminapp:category_list')

    def get_success_url(self):
        return reverse('adminapp:product_list', args=[self.kwargs['pk']])


# @user_passes_test(lambda u: u.is_superuser)
# def product_update(request, pk):
#     title = 'продукт/редактирование'
#
#     edit_product = get_object_or_404(Product, pk=pk)
#
#     if request.method == 'POST':
#         edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('adminapp:product_update', args=[edit_product.pk]))
#     else:
#         edit_form = ProductEditForm(instance=edit_product)
#
#     context = {
#         'title': title,
#         'update_form': edit_form,
#         'category': edit_product.category
#     }
#
#     return render(request, 'adminapp/product_update.html', context)

class ProductUpdateView(AccessMixin, UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    fields = '__all__'

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])


# @user_passes_test(lambda u: u.is_superuser)
# def product_delete(request, pk):
#     title = 'продукт/удаление'
#
#     product = get_object_or_404(Product, pk=pk)
#
#     if request.method == 'POST':
#         product.is_active = False
#         product.save()
#         return HttpResponseRedirect(reverse('adminapp:products', args=[product.category.pk]))
#
#     context = {
#         'title': title,
#         'product_to_delete': product
#     }
#
#     return render(request, 'adminapp/product_delete.html', context)

class ProductDeleteView(AccessMixin, DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])

    # def delete(self, request, *args, **kwargs):
    #     if self.object.is_active:
    #         self.object.is_active = False
    #     else:
    #         self.object.is_active = True
    #     self.object.save()
    #     return HttpResponseRedirect(reverse('adminapp:product_list', args=[self.objectproduct_item.category_id]))