from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .models import Category, Product

def index(request):

    template = loader.get_template('product/index.html')
    return HttpResponse(template.render(request=request))

def search(request):

    if request.method == 'POST':
        query = request.POST.get('query')
        category = request.POST.get('category')
        if not query:
            products = Product.objects.filter(category=category)[:6]
        else:
            products = Product.objects.filter(category=category).filter(name__icontains=query)[:6]
        context = {"products": products}
        template = loader.get_template('product/results.html')
        return HttpResponse(template.render(context, request=request))

def user_page(request):

    if request.user.is_authenticated:
        context = {"user_name": request.user.username}
        template = loader.get_template('product/user.html')
        return HttpResponse(template.render(context, request=request))
    else:
        template = loader.get_template('product/login.html')
        return HttpResponse(template.render(request=request))

def create_user(request):

    if request.method == 'POST':
        create_username = request.POST.get('create_username')
        create_email = request.POST.get('create_email')
        create_password = request.POST.get('create_password')
        if create_username and create_email and create_password:
            if User.objects.filter(email=create_email).exists():
                context = {"error": "Cet email est déjà utilisé."}
            elif User.objects.filter(username=create_username).exists():
                context = {"error": "Ce pseudo est déjà utilisé."}
            else:
                User.objects.create_user(
                    email=create_email,
                    username=create_username,
                    password=create_password
                )
                context = {"created": "Votre compte a été crée, connectez vous!"}
        else:
            context = {"error": "Remplissez tous les champs."}
        template = loader.get_template('product/login.html')
        return HttpResponse(template.render(context, request=request))

def connect_user(request):

    if request.method == 'POST':
        login_username = request.POST.get('login_username')
        login_password = request.POST.get('login_password')
        if login_username and login_password:
            if User.objects.filter(username=login_username).exists():
                user = authenticate(username=login_username, password=login_password)
                if user is not None:
                    login(request, user)
                    context = {"user_name": request.user.username}
                    template = loader.get_template('product/user.html')
                    return HttpResponse(template.render(context, request=request))
                else:
                    context = {"error": "Le mot de passe est incorrect."}
                    template = loader.get_template('product/login.html')
                    return HttpResponse(template.render(context, request=request))
            else:
                context = {"error": "L'utilisateur n'existe pas."}
                template = loader.get_template('product/login.html')
                return HttpResponse(template.render(context, request=request))
        else:
            context = {"error": "Remplissez tous les champs."}
            template = loader.get_template('product/login.html')
            return HttpResponse(template.render(context, request=request))

def save(request):

    if request.method == 'POST':
        product_to_save = request.POST.get('product_id')
        product_obj = Product(id=product_to_save)
        print(product_obj)
        product_obj.user.add(request.user.id)
        template = loader.get_template('product/index.html')
        return HttpResponse(template.render(request=request))

def user_logout(request):

    logout(request)
    template = loader.get_template('product/index.html')
    return HttpResponse(template.render(request=request))
