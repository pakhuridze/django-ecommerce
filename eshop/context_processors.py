def cart_context(request):
    if request.user.is_authenticated:
        from .models import CartItem
        cart_items_count = CartItem.objects.filter(cart__user=request.user).count()
    else:
        cart_items_count = 0

    return {
        'cart_items_count': cart_items_count
    }