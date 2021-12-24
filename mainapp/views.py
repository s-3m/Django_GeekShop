from random import shuffle, choice
from django.shortcuts import render, get_object_or_404
from .models import Product, ProductCategory
from basketapp.models import Basket

# Create your views here.


# with open('mainapp/main_menu.json', 'r', encoding='utf-8') as menu_file:
#     main_menu_links_dict = json.load(menu_file)
# main_menu_links = [i for i in main_menu_links_dict['menu_links']]
main_menu_links = [
    {"href": "main", "name": "Главная"},
    {"href": "products:index", "name": "Продукты"},
    {"href": "contact", "name": "Контакты"},
]


def all_prod():
    all_products = Product.objects.all()
    my_list = list(all_products)
    shuffle(my_list)
    return my_list[0:4]


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_hot_product():
    products = Product.objects.all()

    return choice(list(products))


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category). \
                        exclude(pk=hot_product.pk)[:3]

    return same_products


def index(request):
    basket = Basket.objects.filter(user=request.user)
    total_cost = sum(i.product.price for i in basket)

    return render(request, 'mainapp/index.html', context={'main_menu_links': main_menu_links,
                                                          'products': all_prod(),
                                                          'basket': basket,
                                                          'total_cost': total_cost})


def products(request, pk=None):
    title = "продукты"
    prod_menu_links = ProductCategory.objects.all()
    # related_products = all_prod()[:3] if not pk else Product.objects.filter(
    #     category__id=pk)
    hot_product = get_hot_product()
    same_product = get_same_products(hot_product)
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    total_cost = sum(i.product.price for i in basket)

    if pk is not None:
        if pk == 0:
            all_products = Product.objects.all().order_by("price")
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            all_products = Product.objects.filter(category__pk=pk).order_by('price')

        return render(request, 'mainapp/products_list.html', context={'main_menu_links': main_menu_links,
                                                                      'prod_menu_links': prod_menu_links,
                                                                      'title': title,
                                                                      'category': category,
                                                                      'all_products': all_products,
                                                                      'total_cost': total_cost,
                                                                      'basket': basket,})

    if pk:
        if pk == '0':
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        return render(request, 'mainapp/products_list.html', context={'title': title,
                                                                      'links_menu': prod_menu_links,
                                                                      'category': category,
                                                                      'products': products,
                                                                      'basket': basket,
                                                                      'total_cost': total_cost})

    return render(request, 'mainapp/products.html', context={'main_menu_links': main_menu_links,
                                                             'prod_menu_links': prod_menu_links,
                                                             'hot_product': hot_product,
                                                             'same_product': same_product,
                                                             'basket': basket,
                                                             'total_cost': total_cost,
                                                             'title': title})


def product(request, pk):
    title = 'Товар'

    return render(request, 'mainapp/product.html', context={'title': title,
                                                            'links_menu': ProductCategory.objects.all(),
                                                            'product': get_object_or_404(Product, pk=pk),
                                                            'basket': get_basket(request.user),
                                                            'main_menu_links': main_menu_links})


def contact(request):
    basket = Basket.objects.filter(user=request.user)
    total_cost = sum(i.product.price for i in basket)
    return render(request, 'mainapp/contact.html', context={'main_menu_links': main_menu_links,
                                                            'basket': basket,
                                                            'total_cost': total_cost})
