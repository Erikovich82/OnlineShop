from django.contrib import admin

from .models import *

from mptt.admin import DraggableMPTTAdmin
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_filed = 'title'
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_filter = ['status']
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug':('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'

class ProductImageInline(admin.TabularInline):
    model = Images
    extra = 5

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','category','status','image_tag']
    list_filter = ['category']
    readonly_fields = ('image_tag',)
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug':('title',)}

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['product','title','image_tag',]
    list_filter = ['product']
    readonly_fields = ('image_tag',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['status','subject','user','update_at',]
    list_filter = ['status','user']
    readonly_fields = ('comment','subject','user','ip','rate','product')

admin.site.register(Comment,CommentAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Images,ImagesAdmin)
