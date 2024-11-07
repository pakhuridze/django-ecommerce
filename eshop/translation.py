from modeltranslation.translator import register, TranslationOptions
from .models import Product
from .models import Category

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'country_of_origin', 'quality')
    required_languages = ('ka', 'en')

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

    required_languages = ('ka', 'en')