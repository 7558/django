from django.shortcuts import render
from .models import ProductCategory, Product


def index(request):
    title = 'главная'

    products = Product.objects.all()[:4]

    content = {'title': title, 'products': products}

    return render(request, 'mainapp/index.html',  content)


def contact(request):
    context = {
        'title': 'Контакты'
    }
    return render(request, 'mainapp/contact.html', context)


def products(request, pk=None):
    context = {
        "links_menu": ProductCategory.objects.all(),
        'title': 'Продукты'

    }
    return render(request, 'mainapp/products.html', context=context)
