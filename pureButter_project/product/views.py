import logging
from django.shortcuts import get_list_or_404
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Product

logger = logging.getLogger(__name__)

def index(request):

    template = loader.get_template('product/index.html')
    return HttpResponse(template.render(request=request))

def search(request):

    if request.method == 'POST':
        query = request.POST.get('query')
        category = request.POST.get('category')
        if not query:
            products = get_list_or_404(Product.objects.order_by(
                'nutrition_grades'), category=category)[:6]
        else:
            products = get_list_or_404(Product.objects.order_by(
                'nutrition_grades'), category=category,
                                       name__icontains=query)[:6]
        context = {"products": products, "query": query, "category":category}
        template = loader.get_template('product/results.html')
        logger.info('New search', exc_info=True, extra={
            'request': request,
        })
        return HttpResponse(template.render(context, request=request))
    else:
        template = loader.get_template('product/index.html')
        return HttpResponse(template.render(request=request))

def user_page(request):

    if request.user.is_authenticated:
        context = {"user_name": request.user.username,
                   "user_email": request.user.email}
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
                context = {"errorc": "Cet email est déjà utilisé."}
            elif User.objects.filter(username=create_username).exists():
                context = {"errorc": "Ce pseudo est déjà utilisé."}
            else:
                User.objects.create_user(
                    email=create_email,
                    username=create_username,
                    password=create_password)
                context = {"created":
                           "Votre compte a été crée, connectez vous!"}
        else:
            context = {"errorc": "Remplissez tous les champs."}
        template = loader.get_template('product/login.html')
        return HttpResponse(template.render(context, request=request))
    else:
        template = loader.get_template('product/index.html')
        return HttpResponse(template.render(request=request))

def connect_user(request):

    if request.method == 'POST':
        login_username = request.POST.get('login_username')
        login_password = request.POST.get('login_password')
        if login_username and login_password:
            if User.objects.filter(username=login_username).exists():
                user = authenticate(username=login_username,
                                    password=login_password)
                if user is not None:
                    login(request, user)
                    context = {"user_name": request.user.username,
                               "user_email": request.user.email}
                    template = loader.get_template('product/user.html')
                    return HttpResponse(template.render(context,
                                                        request=request))
                else:
                    context = {"errorl": "Le mot de passe est incorrect."}
                    template = loader.get_template('product/login.html')
                    return HttpResponse(template.render(context,
                                                        request=request))
            else:
                context = {"errorl": "L'utilisateur n'existe pas."}
                template = loader.get_template('product/login.html')
                return HttpResponse(template.render(context, request=request))
        else:
            context = {"errorl": "Remplissez tous les champs."}
            template = loader.get_template('product/login.html')
            return HttpResponse(template.render(context, request=request))
    else:
        template = loader.get_template('product/index.html')
        return HttpResponse(template.render(request=request))

def save(request):

    if request.method == 'POST':
        product_to_save = request.POST.get('product_id')
        product_obj = Product(id=product_to_save)
        product_obj.user.add(request.user.id)
        product = Product.objects.get(id=product_to_save)
        registered = True
        nutripicture = "product/img/n" + product.nutrition_grades + ".png"
        context = {"product": product, "nutripicture": nutripicture,
                   "registered": registered}
        template = loader.get_template('product/product.html')
        return HttpResponse(template.render(context, request=request))
    else:
        template = loader.get_template('product/index.html')
        return HttpResponse(template.render(request=request))

def product_page(request, product_id):

    product = Product.objects.get(id=product_id)
    registered = False
    user_products = Product.objects.filter(user=request.user.id)
    for item in user_products:
        if item.id == int(product_id):
            registered = True
    nutripicture = "product/img/n" + product.nutrition_grades + ".png"
    context = {"product": product, "nutripicture": nutripicture,
               "registered": registered}
    template = loader.get_template('product/product.html')
    return HttpResponse(template.render(context, request=request))

def user_product(request):

    products = Product.objects.filter(user=request.user.id).order_by('id')
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)
    context = {"products": product, "paginate": True}
    template = loader.get_template('product/myproduct.html')
    return HttpResponse(template.render(context, request=request))

def user_logout(request):

    logout(request)
    template = loader.get_template('product/index.html')
    return HttpResponse(template.render(request=request))

def legal_notice(request):

    template = loader.get_template('product/legalnotice.html')
    return HttpResponse(template.render(request=request))
