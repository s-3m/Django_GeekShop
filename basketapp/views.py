from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse

from basketapp.models import Basket
from mainapp.models import Product
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import F



@login_required
def basket(request):
    title = 'Корзина'
    basket_items = Basket.objects.filter(user=request.user).order_by('product__category').select_related()
    content = {'basket_items': basket_items, 'title': title}
    return render(request, 'basketapp/basket.html', content)


@login_required
def basket_add(request, pk):

    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))
    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).select_related().first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    # basket.quantity += 1
    # basket.save()
    basket.quantity = F('quantity') + 1

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_edit(request, pk, quantity):
    def is_ajax(request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    if is_ajax(request=request):
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_item = Basket.objects.filter(user=request.user).order_by('product__category').select_related()
        content = {'basket_items': basket_item}

        result = render_to_string('basketapp/include/inc_basket_list.html', content)

        return JsonResponse({'result': result})