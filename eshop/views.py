from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem, Product,  Tag, Category


# Create your views here.
def index(request):
    cart_items_count = CartItem.objects.filter(cart__user=request.user).count()
    print(cart_items_count)
    return render(request, 'index.html', {'cart_items_count': cart_items_count})



def contact(request):
    return render(request, 'contact.html')



def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))
        action = request.POST.get("action")

        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if action == "add":
            if created:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity
            cart_item.save()

        elif action == "increase":
            cart_item.quantity += 1
            cart_item.save()

        elif action == "decrease":
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()

        elif action == "remove":
            cart_item.delete()

        return redirect('eshop:cart')

    cart_items_with_total = [
        {
            'item': item,
            'total_price': item.product.price * item.quantity
        }
        for item in cart_items
    ]

    total_price = sum(item['total_price'] for item in cart_items_with_total)

    return render(request, 'cart.html', {
        'cart_items_with_total': cart_items_with_total,
        'total_price': total_price,
    })


def product(request, slug):
    get_product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop_detail.html', {'product': get_product})


def checkout(request):
    return render(request, 'checkout.html')


def category(request, slug=None):
    tag_filter = request.GET.get('tag')
    max_price = request.GET.get('max_price', 500)
    search_query = request.GET.get('search', '')

    if slug is None or slug == 'all':
        products = Product.objects.all().order_by('id')
    else:
        category_obj = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=category_obj).order_by('id')

    if search_query:
        products = products.filter(name__icontains=search_query)

    if tag_filter:
        tag_obj = get_object_or_404(Tag, name=tag_filter)
        products = products.filter(tags=tag_obj)

    products = products.filter(price__lte=max_price)

    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    paginated_products = paginator.get_page(page_number)

    categories = Category.objects.all()
    tags = Tag.objects.all()

    context = {
        'products': paginated_products,
        'categories': categories,
        'tags': tags,
        'max_price': max_price,
        'selected_tag': tag_filter,
        'search_query': search_query,
    }

    return render(request, 'shop.html', context)


