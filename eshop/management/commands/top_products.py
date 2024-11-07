from django.core.management.base import BaseCommand
from eshop.models import Product, CartItem
from django.db.models import Count

class Command(BaseCommand):
    help = 'Find the top 3 most popular products in users’ carts'

    def handle(self, *args, **kwargs):
        # Aggregate count of users per product and get top 3
        top_products = (
            Product.objects
            .annotate(user_count=Count('cartitem__cart__user', distinct=True))
            .order_by('-user_count')[:3]
        )

        if not top_products:
            self.stdout.write(self.style.WARNING("No products found in any cart."))
        else:
            self.stdout.write(self.style.SUCCESS("Top 3 most popular products in users’ carts:"))
            for product in top_products:
                self.stdout.write(f"{product.name} - {product.user_count} users")
