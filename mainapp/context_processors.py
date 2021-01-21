from basketapp.models import Basket


def basket(request):
    basket_item = []

    if request.user.is_authenticated:
        basket_item = Basket.objects.filter(user=request.user).select_related()

    return {
        'basket': basket_item
    }
