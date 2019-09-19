from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Category, Product
from .forms import CreateUser

def index(request):
    template = loader.get_template('product/index.html')
    return HttpResponse(template.render(request=request))

def results(request):
    products = Product.objects.order_by('id')[:6]
    context = {
        'products': products
    }
    template = loader.get_template('product/results.html')
    return HttpResponse(template.render(context, request=request))

def login(request):
    if request.user.is_authenticated:
        template = loader.get_template('product/user.html')
        return HttpResponse(template.render(request=request))
    else:
        if request.method == 'POST':
            form = CreateUser(request.POST)
            if form.is_valid():
                username = request.POST.get('login')
                email = request.POST.get('email')
                password = request.POST.get('password')
            mail = User.objects.filter(email=email)
            if not mail.exists():
                User.objects.create_user(
                    email=email,
                    username=username,
                    password=password
                )
        else:
            form = CreateUser()
        return render(request, 'product/login.html', {'form': form})
