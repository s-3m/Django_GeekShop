from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from authapp.forms import ShopUserRegisterForm
from adminapp.forms import ProductEditForm, ShopUserAdminEditForm, ProductCategoryEditForm
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.dispatch import receiver
from django.db.models.signals import pre_save


# Create your views here.

class UserListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    paginate_by = 2

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'user/create'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'user/update'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin:users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductCategoryList(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/добавление'
        return context




class ProductCategoryUpdate(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context




class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())




class ProductsListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'
    paginate_by = 2

    def get_queryset(self):
        if self.kwargs['pk'] != 0:
            return Product.objects.filter(category__id=self.kwargs['pk'])
        else:
            return Product.objects.all()

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукты/категории'
        context['category'] = self.kwargs['pk']
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('admin:products', args=[self.kwargs['pk']])

    def get_initial(self):
        initial = super().get_initial()
        initial['category'] = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        return initial

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'product/create'
        context['category'] = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def product_create(request, pk):
#     title = 'Новый продукт'
#     category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         product_form = ProductEditForm(request.POST, request.FILES)
#         if product_form.is_valid():
#             product_form.save()
#             return HttpResponseRedirect(reverse('admin:products', args=[pk]))
#     else:
#         product_form = ProductEditForm(initial={'category': category})
#
#     content = {'title': title, 'category': category, 'update_form': product_form}
#     return render(request, 'adminapp/product_update.html', content)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'


# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     title = 'Подробно о продукте'
#     product = get_object_or_404(Product, pk=pk)
#     content = {'title': title, 'object': product}
#     return render(request, 'adminapp/product_read.html', content)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('admin:products', args=[self.kwargs['pk']])

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'product/update'
        context['category'] = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        context['category_id'] = self.kwargs['pk']
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def product_update(request, pk):
#     title = 'Редактор продукта'
#     edit_product = get_object_or_404(Product, pk=pk)
#
#     if request.method == 'POST':
#         edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin:product_update', args=[pk]))
#     else:
#         edit_form = ProductEditForm(instance=edit_product)
#
#     content = {'title': title, 'category': edit_product.category, 'update_form': edit_form}
#     return render(request, 'adminapp/product_update.html', content)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_success_url(self):
        return reverse_lazy('admin:products', args=[self.object.category.id])

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

# @user_passes_test(lambda u: u.is_superuser)
# def product_delete(request, pk):
#     title = 'Удаление продукта'
#     product = get_object_or_404(Product, pk=pk)
#
#     if request.method == 'POST':
#         product.is_active = False
#         product.save()
#         return HttpResponseRedirect(reverse('admin:products', args=[product.category.pk]))
#
#     content = {'title': title, 'product_on_delete': product}
#     return render(request, 'adminapp/product_delete.html', content)


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

