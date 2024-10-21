from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from eshop.models import Category, Product


# Create your views here.
def index(request):
    return render(request, 'index.html')


def contact(request):
    return render(request, 'contact.html')


def cart(request):
    return render(request, 'cart.html')


def product(request, slug):
    get_product = get_object_or_404(Product, slug=slug)

    return render(request, 'shop_detail.html', {'product': get_product})


def checkout(request):
    return render(request, 'checkout.html')



def category(request, slug=None):
    if slug is None or slug == 'all':
        products = Product.objects.all().order_by('id')
    else:
        get_category_obj = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=get_category_obj).order_by('id')

    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    paginated_products = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        'products': paginated_products,
        'categories': categories,
        'paginator': paginator,
    }

    return render(request, 'shop.html', context)
