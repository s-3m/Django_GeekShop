from basketapp.models import Basket


def basket(request):
    basket = []

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user).select_related()
    total_cost = sum(i.product.price for i in basket)


    return {'basket': basket, 'total_cost': total_cost}
