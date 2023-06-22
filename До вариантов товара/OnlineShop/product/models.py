from django.db import models
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from django.urls import reverse
from django.contrib.auth.models import User


class Category(MPTTModel):
    # Кортеж для панели администратора Для выбора статуса
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    #Для создания дерева категорий, мы хотим обозначить взаимосвязи между категориями
    parent = TreeForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image=models.ImageField(blank=True,upload_to='images/')
    status=models.CharField(max_length=10, choices=STATUS) #вот этого статуса
    slug = models.SlugField(null=False, unique=True) #для вызова данных из БД через URL
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    # from django.urls import reverse
    def get_absolute_url(self):
        return reverse('category_detail',
                       kwargs={'slug':self.slug})

    def __str__(self):
        full_path = [self.title]
        cat = self.parent
        while cat is not None:
            full_path.append(cat.title)
            cat = cat.parent
        return ' / '.join(full_path[::-1])

    class MPTTMeta:
        order_insertion_by = ['title']

class Product(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image=models.ImageField(upload_to='images/',null=False)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    amount=models.IntegerField(default=0)
    minamount = models.IntegerField()
    #from ckeditor.fields import RichTextField
    detail = RichTextField()
    slug = models.SlugField(null=False, unique=True)
    status=models.CharField(max_length=10,choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('product_detail',
                       kwargs={'slug':self.slug})

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="100" height="100" />')


class Images(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(max_length= 100, blank = True)
    image = models.ImageField(blank = True, upload_to='images/')

    def __str__(self):
        return self.title

    #from django.utils.safestring import mark_safe
    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="100" height="100" />')



#from django.contrib.auth.models import User
class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=150, blank=True)
    comment = models.CharField(max_length=400, blank=True)
    rate = models.IntegerField(default=5)
    ip = models.CharField(max_length=20, blank = True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
