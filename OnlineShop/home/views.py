from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import Setting, ContactMessage
from .forms import ContactForm
from django.contrib import messages
from product.models import Category, Product
from django.contrib import messages
from order.models import ShopCart
from user.models import UserProfile
from OnlineShop import settings
from django.utils import translation
from django.utils.translation import get_language
from django.utils.translation import gettext as _
from django.conf import settings

def index(request):
    defaultcurr = settings.DEFAULT_CURRENCY
    string_example = _('Demo-text')
    if not request.session.has_key('currency'):
        request.session['currency'] = defaultcurr
    print('Текущая валюта:', request.session['currency'])
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    product_slider = Product.objects.order_by('id').all()[:3] #3 первых
    product_latest = Product.objects.order_by('-id').all()[:4]#4 последних
    random_products = Product.objects.order_by('?').all()[:4] #4 случайных тоавра

    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for element in shopcart:
        if element.variant != None:
            total += element.variant.price * element.quantity
        else:
            total += element.product.price * element.quantity



    context = {'setting': setting, 'category': category,
               'product_slider': product_slider,
               'product_latest': product_latest,
               'random_products':random_products,
               'total':total, 'shopcart': shopcart,
               'string_example':string_example}
    return render(request, 'home/index.html', context)


def search(request):
    pass

def selectcurrency(request):
    lasturl = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        request.session['currency'] = request.POST['currency']
        data = UserProfile.objects.get(user_id=request.user.id)
        data.currency_id = request.session['currency']
    return HttpResponseRedirect(lasturl)

def aboutus(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for element in shopcart:
        if element.variant != None:
            total += element.variant.price * element.quantity
        else:
            total += element.product.price * element.quantity



    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'total':total, 'shopcart': shopcart,'setting': setting, 'category': category }
    return render(request, 'home/about.html', context)
    # return HttpResponse('<h1> aboutus  </h1>')

def contacts(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for element in shopcart:
        if element.variant != None:
            total += element.variant.price * element.quantity
        else:
            total += element.product.price * element.quantity


    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid(): #прошли валидацию
            data = ContactMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
#from django.contrib import messages
#from django.shortcuts import render, HttpResponse, HttpResponseRedirect
            messages.success(request,'Сообщение отправлено!')
            return HttpResponseRedirect('/contacts')
    form = ContactForm
    context = {'shopcart': shopcart, 'total':total, 'setting': setting, 'form':form , 'category': category }
    return render(request, 'home/contacts.html', context)

def selectlanguage(request):


    if request.method == 'POST':
        current_language = translation.get_language()
        lasturl = request.META.get('HTTP_REFERER')
        lang = request.POST['language']
        translation.activate(lang)
        response = HttpResponseRedirect("/"+lang)
        request.session[settings.LANGUAGE_SESSION_KEY] = lang
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME,lang)

    return response