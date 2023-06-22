from modeltranslation.translator import register,translator, TranslationOptions
from .models import *

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

translator.register(Product, ProductTranslationOptions)