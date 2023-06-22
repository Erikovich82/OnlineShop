from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from home.models import Setting
from .models import Category, Product
from .forms import CommentForm
import json
from django.contrib import messages
from django.shortcuts import render, HttpResponse, HttpResponseRedirect

from .models import *
from order.models import ShopCart
def product_detail(request, id, slug):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for element in shopcart:
        total += element.product.price * element.quantity



    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    product = Product.objects.filter(pk=id)[0]
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    average_rate = 0
    for c in comments:
        average_rate+= c.rate
    if len(comments) != 0:
        average_rate /= len(comments)
        average_rate = round(average_rate,3)
    else:
        average_rate = ' '
    context = {'shopcart': shopcart, 'total': total,'setting': setting, 'category': category,
               'product': product, 'images': images,
               'comments':comments, 'average_rate': average_rate}

    return render(request, 'product/product_page.html', context)


def search_auto(request):
    print('######################################### РАБОТАТЕТ!')
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)
        results = []
        for p in products:
            product_json = {}
            product_json = p.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

# Create your views here.
def index(request):
    # return render(request, 'home/index.html')
    return HttpResponse('<h1> Product index </h1>')


# from home.models import Setting
# from .models import Category, Product
def category_product(request, id, slug):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for element in shopcart:
        total += element.product.price * element.quantity



    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    products = Product.objects.filter(category_id=id)
    current_category = Category.objects.filter(id=id)[0]
    print(current_category)
    context = {'shopcart': shopcart, 'total': total,'setting': setting, 'category': category,
               'products': products, 'current_category': current_category}

    return render(request, 'product/category_product.html', context)


from .forms import SearchForm


def search(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for element in shopcart:
        total += element.product.price * element.quantity



    print(request.POST)
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if request.POST['query']=='':
            query = 'All products'
            catid = -1
        else:
            query = request.POST['query']
            catid = int(request.POST['catid'])

        if catid == 0:  # все категории
            products = Product.objects.filter(title__icontains=query)
        elif catid == -1: #человек сделал поиск с пустым окном
            products = Product.objects.all()
        else:
            products = Product.objects.filter(category_id=catid, title__icontains=query)

        setting = Setting.objects.get(pk=1)
        category = Category.objects.all()
        context = {    'shopcart': shopcart, 'total': total,'setting': setting, 'category': category, 'query': query, 'products': products}
        return render(request, 'product/search_product.html', context)
    return HttpResponseRedirect('/')

# from .forms import CommentForm
def addcomment(request,id):
    product = Product.objects.get(pk=id)
    url = f'/product/{product.id}/{product.slug}' #последний URL_адрес
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():  # прошли валидацию
            data = Comment()
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id = id
            current_user = request.user
            data.user_id = current_user.id
            data.save()
            # from django.contrib import messages
            # from django.shortcuts import render, HttpResponse, HttpResponseRedirect
            messages.success(request, 'Review commited!')
            return HttpResponseRedirect(url)
