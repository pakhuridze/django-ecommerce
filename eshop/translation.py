from modeltranslation.translator import register, TranslationOptions
from .models import Product

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'country_of_origin')
    required_languages = ('en', 'ka')