from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from mptt.models import MPTTModel, TreeForeignKey
from versatileimagefield.fields import VersatileImageField, PPOIField

class Category(MPTTModel):
    name = models.CharField(max_length=200, verbose_name="სახელი")
    slug = models.SlugField(unique=True, max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                            verbose_name="კატეგორია")

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    category = TreeForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = VersatileImageField(upload_to='products/', null=True, blank=True,)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    country_of_origin = models.CharField(max_length=255, blank=True, null=True)
    quality = models.CharField(max_length=50, choices=[('Organic', 'Organic'), ('Non-Organic', 'Non-Organic')])
    min_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='products')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    review = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.product.name}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    cart = models.OneToOneField(Cart, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,
                              choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Completed', 'Completed'),
                                       ('Canceled', 'Canceled')], default='Pending')

    def __str__(self):
        return f"Order {self.id} by {self.user.username if self.user else 'Guest'}"
