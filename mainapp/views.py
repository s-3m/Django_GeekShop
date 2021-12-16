
from django.shortcuts import render
import json
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


def index(request):

    return render(request, 'mainapp/index.html', context={'main_menu_links': main_menu_links})


def products(request, pk=None):
    related_products = all_prod()[:3] if not pk else Product.objects.filter(
        category__id=pk)
    prod_menu_links = ProductCategory.objects.all()
    print(pk)
    return render(request, 'mainapp/products.html', context={'main_menu_links': main_menu_links,
                                                             'prod_menu_links': prod_menu_links,
                                                             'related_products': related_products})


def contact(request):
    return render(request, 'mainapp/contact.html', context={'main_menu_links': main_menu_links})
