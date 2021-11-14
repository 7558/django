from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product
from basketapp.models import Basket
import random


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    return None


def get_hot_product():
    return random.sample(list(Product.objects.all()), 1)[0]


def get_same_product(hot_product):
    products_list = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return products_list


def index(request):
    title = 'главная'

    products = Product.objects.all()[:4]

    content = {
        'title': title,
        'products': products,
        'basket': get_basket(request.user)
    }

    return render(request, 'mainapp/index.html',  content)


def contact(request):
    context = {
        'title': 'Контакты',
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/contact.html', context)


def products(request, pk=None, page=1):

    title = 'продукты'
    links_menu = ProductCategory.objects.all()

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    if pk is not None:
        if pk == 0:
            products = Product.objects.all()
            category = {
                'name': 'все',
                'pk': 0
            }
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk)

        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,
            'basket': basket,
        }

        return render(request, 'mainapp/products_list.html', context)

    hot_product = get_hot_product()
    same_product = get_same_product(hot_product)

    context = {
        'title': title,
        'links_menu': links_menu,
        'same_product': same_product,
        'hot_product': hot_product,
        'basket': get_basket(request.user)

    }
    return render(request, 'mainapp/products.html', context)

def product(request, pk):
    title = 'продукты'

    context = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user)
    }

    return render(request, 'mainapp/product.html', context)