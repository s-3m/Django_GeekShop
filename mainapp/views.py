from random import shuffle, choice
from django.shortcuts import render, get_object_or_404
from .models import Product, ProductCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from social_core.backends.vk import VKOAuth2

# Create your views here.

main_menu_links = [
    {"href": "main", "name": "Главная"},
    {"href": "products:index", "name": "Продукты"},
    {"href": "contact", "name": "Контакты"},
]


def all_prod():
    all_products = Product.objects.filter(is_active=True).select_related()[:3]
    my_list = list(all_products)
    shuffle(my_list)
    return my_list


def get_hot_product():
    products = Product.objects.filter(is_active=True)

    return choice(list(products))


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk, is_active=False).select_related()[:3]

    return same_products


def index(request):
    return render(request, 'mainapp/index.html', context={'main_menu_links': main_menu_links,
                                                          'products': all_prod(),
                                                          'title': 'главная'})


def products(request, pk=None, page=1):
    title = "продукты"
    prod_menu_links = ProductCategory.objects.all()
    hot_product = get_hot_product()
    same_product = get_same_products(hot_product)
    # pdb.set_trace()
    if pk is not None:
        if pk == '0':
            category = {'pk': 0, 'name': 'все'}
            products = Product.objects.filter(is_active=True,
                                              category__is_active=True).order_by('price').select_related()


        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk, is_active=True).order_by('price').select_related()

        paginator = Paginator(products, 4)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        return render(request, 'mainapp/products_list.html', context={'main_menu_links': main_menu_links,
                                                                      'prod_menu_links': prod_menu_links,
                                                                      'title': title,
                                                                      'category': category,
                                                                      'products': products_paginator})

    return render(request, 'mainapp/products.html', context={'main_menu_links': main_menu_links,
                                                             'prod_menu_links': prod_menu_links,
                                                             'hot_product': hot_product,
                                                             'same_product': same_product,
                                                             'title': title})


def product(request, pk):
    title = 'Товар'

    return render(request, 'mainapp/product.html', context={'title': title,
                                                            'links_menu': ProductCategory.objects.all(),
                                                            'product': get_object_or_404(Product, pk=pk),
                                                            # 'basket': get_basket(request.user),
                                                            'main_menu_links': main_menu_links})


def contact(request):
    return render(request, 'mainapp/contact.html', context={
        'main_menu_links': main_menu_links})
