from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from home.models import Setting
from product.models import Category
from order.models import ShopCart
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from order.models import Order, OrderProduct



def index(request):
    return HttpResponse('<h1> User app </h1>')


@login_required(login_url='/login')
def user_orderdetail(request, id):
    current_user = request.user

    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for element in shopcart:
        total += element.product.price * element.quantity

    orders = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id = id)
    context = {'setting': setting, 'category': category,
               'total': total, 'shopcart': shopcart,
               'order': orders, 'orderitems':orderitems }

    return render(request,'user/user_order_details.html',context)



#from order.models import Order
@login_required(login_url='/login')
def user_orders(request):
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id)
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for element in shopcart:
        total += element.product.price * element.quantity


    context = {'setting': setting, 'category': category,
               'total': total, 'shopcart': shopcart,
               'orders': orders }
    return render( request,'user/user_orders.html',context)


def user_deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment deleted...')
    return HttpResponseRedirect('/user/comments')


def user_deletecomment(request,id)



def user_order_product(request):
    current_user = request.user
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for element in shopcart:
        total += element.product.price * element.quantity

    order_products = OrderProduct.objects.filter(user_id=current_user.id).order_by('-id')



    context = {'setting': setting, 'category': category,
               'total': total, 'shopcart': shopcart,
               'order_products':order_products }

    return render(request, 'user/user_products.html', context)


def user_comments(request):

    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for element in shopcart:
        total += element.product.price * element.quantity

    comments = Comment.objects.filter(user_id=current_user.id)

    context = {'setting': setting, 'category': category,
               'total': total, 'shopcart': shopcart,
               'comments': comments}
    return render(request, 'user/user_comments.html', context)



@login_required(login_url='/login')
def user_update(request):
    current_user = request.user
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance = current_user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES,
                                         instance = current_user.userprofile)


        # !!! Не сохраняется новая фотография
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            # user_profile = UserProfile.objects.get(user_id=current_user.id)
            #
            # print('ФАЙЛЫ ИЗ ЗАПРОСА!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            # print(request.FILES)

            # user_profile.image = request.POST
            # user_profile.save()

            messages.success(request,'Your account has been updated!')
            return HttpResponseRedirect('/user/myaccount')
    else:
        setting = Setting.objects.get(pk=1)
        category = Category.objects.all()
        current_user = request.user
        shopcart = ShopCart.objects.filter(user_id=current_user.id)
        total = 0
        for element in shopcart:
            total += element.product.price * element.quantity

        user_form = UserUpdateForm(instance = request.user)
        profile_form = ProfileUpdateForm(instance = current_user.userprofile)


        context = {'setting': setting, 'category': category,
                   'total': total, 'shopcart': shopcart,
                   'user_form':user_form,'profile_form':profile_form}

        return render(request, 'user/user_update.html', context)


    return HttpResponse('<h1> User_update page </h1>')


#from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
@login_required(login_url='/login')
def password_update(request):

    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request,'Your password was successfully updated!')
            return HttpResponseRedirect('/user/myaccount')
        else:
            messages.warning(request,str(form.errors))

            return HttpResponseRedirect('/user/password')

    form = PasswordChangeForm(user=request.user)
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user

    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for element in shopcart:
        total += element.product.price * element.quantity
    context = {'setting': setting, 'category': category,
               'total': total, 'shopcart': shopcart,
               'form':form}

    return render(request,'user/password_update.html',context)





def login_form(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for element in shopcart:
        total += element.product.price * element.quantity
#from django.contrib.auth import authenticate, login, logout
#from django.contrib import messages
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username,
                            password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,
                             'Login Error, check username or password')
            return HttpResponseRedirect('/user/login')


    context = {'setting': setting, 'category': category,
           'total': total, 'shopcart': shopcart}

    return render(request,'user/login_form.html',context)



def register(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username,
                                password=password)

            login(request,user)
            data = UserProfile()
            data.user_id = user.id
            data.image = 'images/users/user.jpg'
            data.save()
            messages.success(request,'Your account has been created!')
            return HttpResponseRedirect('/')
    form = SignUpForm()
    context = {'setting': setting, 'category': category,
               'form': form }
    return render(request, 'user/signup_form.html', context)

def myaccount(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for element in shopcart:
        total += element.product.price * element.quantity


    context = {'setting': setting, 'category': category,
           'total': total, 'shopcart': shopcart,
               'profile' : profile}
    return render(request, 'user/user_profile.html', context)


def wishlist(request):
    return HttpResponse('<h1> Тут мог быть ваш список хотелок </h1>')

def logout_func(request):
    logout(request)
    return HttpResponseRedirect('/')