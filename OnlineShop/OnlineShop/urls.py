"""
URL configuration for OnlineShop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home import views as home_views
from product import views as product_views
from order import views as order_views
from user import views as user_views
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('selectlanguage/', home_views.selectlanguage, name='selectlanguage'),
    path('18n/', include('django.conf.urls.i18n')),
]
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('home/',include('home.urls')),
    path('order/', include('order.urls')),
    path('user/', include('user.urls')),
    path('product/', include('product.urls')),
    path('currencies/', include('currencies.urls')),
    path('search/', product_views.search,name='search'),
    path('faq/', user_views.faq,name='faq'),
    path('selectlanguage/', home_views.selectlanguage, name='selectlanguage'),
    path('selectcurrency/', home_views.selectcurrency,name='selectcurrency'),
    path('shopcart/', order_views.shopcart, name='shopcart'),
    path('search_auto/', product_views.search_auto, name='search_auto'),
    path('category/<int:id>/<slug:slug>', product_views.category_product, name='category_products'),
    path('about/', home_views.aboutus, name = 'aboutus'),
    path('contacts/',home_views.contacts, name = 'contacts'),
    path('', home_views.index, name='homepage'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


