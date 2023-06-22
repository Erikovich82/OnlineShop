from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from .models import ShopCart
from .forms import ShopCartForm
from django.contrib.auth.decorators import login_required
from home.models import Setting
from product.models import Category, Product, Images, Comment
from .models import Order, OrderProduct
from django.utils.crypto import get_random_string
# Create your views here.
def index(request):
    return HttpResponse('Страница Order')


from .forms import OrderForm

# from .models import Order, OrderProduct
# from django.utils.crypto import get_random_string
def orderproduct(request):
    current_user = request.user
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    form = OrderForm()
    for element in shopcart:
        total += element.product.price * element.quantity
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid() and total !=0:
            # В ЭТОМ МЕСТЕ ВАЖНО ПРОВЕРИТЬ ОПЛАТУ!
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.country = form.cleaned_data['country']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5)
            data.code = ordercode
            data.save()

            #переносим товары из корзины в заказ
            for s in shopcart:
                detail = OrderProduct()
                detail.order_id = data.id
                detail.product_id = s.product_id
                detail.quantity = s.quantity
                detail.price = s.product.price
                detail.amount = s.amount
                detail.user_id = current_user.id
                detail.save() #заказ сформирован - сохраняем
                product = Product.objects.get(id=s.product.id)
                product.amount -= s.quantity
                product.save() #уменьшили количество товара на складе
            shopcart.delete()
            request.session['cart_items'] = 0
            messages.success(request,f'Your order confirmed, thank you! \n Order number:{ordercode}')
            return render(request, 'order/order_complete.html',{'setting': setting, 'category': category,
               'shopcart': shopcart, 'total': total,
               'user':current_user,'ordercode':ordercode}) #context Сюда
        else:
            messages.warning(request, form.errors)


    context = {'setting': setting, 'category': category,
               'shopcart': shopcart, 'total': total,
               'form':form}
    return render(request, 'order/order_form.html', context)


def deletefromcart(request,id):
    url = request.META.get('HTTP_REFERER')
    shopcart = ShopCart.objects.get(pk = id)
    name = shopcart.product.title
    shopcart.delete()
    messages.success(request,
                     f'Item {name} was succesfully deleted from Shopcart')
    return HttpResponseRedirect(url)





@login_required(login_url='/login')
def addtoshopcart(request,id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    checkproduct = ShopCart.objects.filter(product_id=id)

    if checkproduct: control = 1 #товар в корзине
    else: control = 0            #товар не в корзине

    if request.method == "POST":
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1: #Обновляем корзину
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
                messages.success(request, 'Корзина обновлена')
            else: #добавляем в корзину
                data=ShopCart()
                data.user_id = current_user.id
                data.product_id=id
                data.quantity = form.cleaned_data['quantity']
                data.save()
                messages.success(request,'Товар добавлен в корзину')
        return HttpResponseRedirect(url)
    else: #если это не РОST запрос
        if control == 1:
            data= ShopCart.objects.get(product_id=id)
            data.quantity +=1 #если еще раз ткнули добавить тот же товар
            data.save()
            messages.success(request, 'Корзина обновлена')
        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1 #только 1 товар
            data.save()
            messages.success(request,'Товар добавлен в корзину')
        return HttpResponseRedirect(url)




def shopcart(request):
    current_user = request.user
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for element in shopcart:
        total += element.product.price * element.quantity
    print('Общая сумма:',total)
    context = {'setting': setting, 'category': category,
               'shopcart': shopcart, 'total':total}
    return render(request, 'order/shopcart.html', context)