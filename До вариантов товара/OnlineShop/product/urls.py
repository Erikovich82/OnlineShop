from django.contrib import admin
from django.urls import path

from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/<slug:slug>', views.product_detail, name='product_detail'),
    path('addcomment/<int:id>', views.addcomment, name='addcomment'),

]
