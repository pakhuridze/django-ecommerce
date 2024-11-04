from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_cookie

from .models import Cart, CartItem, Product, Tag, Category
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, FormView
from .forms import CartForm, ContactForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

class IndexView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('eshop:contact')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        # Send email to admin
        email_message = f"""
        New contact form submission:

        Name: {name}
        Email: {email}
        Message:
        {message}
        """

        try:
            send_mail(
                subject=f'New Contact Form Submission from {name}',
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list="pakhuridze.tornike@gmail.com",
                fail_silently=False,
            )
            messages.success(self.request, 'Thank you for your message! We will get back to you soon.')
        except Exception as e:
            messages.error(self.request, 'Sorry, there was an error sending your message. Please try again later.')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class CartView(LoginRequiredMixin, FormView):
    template_name = 'cart.html'
    login_url = '/accounts/login/'  # Redirect URL for unauthenticated users

    form_class = CartForm

    def get_cart(self):
        """Retrieve the cart and related items in a single query."""
        return Cart.objects.prefetch_related('items__product').get_or_create(user=self.request.user)[0]

    def get_context_data(self, **kwargs):
        """Add cart items and total price to the context with fewer queries."""
        context = super().get_context_data(**kwargs)
        cart = self.get_cart()

        # Avoid hitting the database repeatedly by using pre-fetched items
        cart_items_with_total = [
            {'item': item, 'total_price': item.product.price * item.quantity}
            for item in cart.items.all()
        ]

        context['cart_items_with_total'] = cart_items_with_total
        context['total_price'] = sum(item['total_price'] for item in cart_items_with_total)
        return context

    def form_valid(self, form):
        """Handle form submission to modify cart items."""
        cart = self.get_cart()
        product_id = form.cleaned_data['product_id']
        quantity = form.cleaned_data['quantity']
        action = form.cleaned_data['action']

        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if action == "add":
            cart_item.quantity = quantity if created else cart_item.quantity + quantity
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


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'checkout.html'
    login_url = '/accounts/login/'  # Redirect URL for unauthenticated users

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve cart items only for logged-in users
        cart_items = CartItem.objects.filter(cart=self.request.user.cart)
        context['cart_items'] = cart_items
        # Calculate total price
        context['total'] = sum(item.product.price * item.quantity for item in cart_items)
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 2

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60 * 10))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        # Get the category slug from the URL
        slug = self.kwargs.get('slug', 'all')
        tag_filter = self.request.GET.get('tag')
        max_price = self.request.GET.get('max_price', 500)
        search_query = self.request.GET.get('search', '')

        # Filter products based on category slug
        # If the slug is 'all', get all products
        if slug is None or slug == 'all':
            queryset = Product.objects.all().order_by('id')
        else:
            # Get the category object based on the slug
            category_obj = get_object_or_404(Category, slug=slug)
            queryset = Product.objects.filter(category=category_obj).order_by('id')

        # Apply search filter
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        # Apply tag filter
        if tag_filter:
            tag_obj = get_object_or_404(Tag, name=tag_filter)
            queryset = queryset.filter(tags=tag_obj)

        # Apply price filter
        queryset = queryset.filter(price__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all categories and tags to display in the template
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()

        # Pass selected filters to the template
        context['max_price'] = self.request.GET.get('max_price', 500)
        context['selected_tag'] = self.request.GET.get('tag')
        context['search_query'] = self.request.GET.get('search', '')

        return context
