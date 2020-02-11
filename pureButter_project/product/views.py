import logging
import re
from django.shortcuts import get_list_or_404
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Product, Profil

logger = logging.getLogger(__name__)

def index(request):

    template = loader.get_template('product/index.html')
    return HttpResponse(template.render(request=request))

def search(request):
    """view called when an user make a research"""

    if request.method == 'POST':
        query = request.POST.get('query')
        category = request.POST.get('category')
        request.session['query'] = query
        request.session['category'] = category
    else:
        query = request.session['query']
        category = request.session['category']
    if request.user.is_authenticated:
        if not query:
            products = get_list_or_404(Product.objects.exclude(
                id__in=Product.objects.filter(user=request.user.id)).order_by(
                    'nutrition_grades'), category=category)
        else:
            products = get_list_or_404(Product.objects.exclude(
                id__in=Product.objects.filter(user=request.user.id)).order_by(
                    'nutrition_grades'), category=category,
                                       name__icontains=query)
    else:
        if not query:
            products = get_list_or_404(Product.objects.order_by(
                'nutrition_grades'), category=category)
        else:
            products = get_list_or_404(Product.objects.order_by(
                'nutrition_grades'), category=category, name__icontains=query)
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)
    context = {"products": product, "paginate": True, "query": query,
               "category":category}
    template = loader.get_template('product/results.html')
    logger.info('New search', exc_info=True, extra={
        'request': request,
    })
    return HttpResponse(template.render(context, request=request))

def user_page(request):
    """view called when a user (any user) request the user page"""

    if request.user.is_authenticated:
        picture_exist = Profil.objects.filter(user=request.user.id)
        if picture_exist.exists():
            picture_exist = Profil.objects.get(user=request.user.id)
            picture = picture_exist.image_url
            regex = re.compile("http:")
            if regex.match(picture) == None:
                picture = False
        else:
            picture = False
        context = {"user_name": request.user.username,
                   "user_email": request.user.email,
                   "picture": picture}
        template = loader.get_template('product/user.html')
        return HttpResponse(template.render(context, request=request))
    else:
        template = loader.get_template('product/login.html')
        return HttpResponse(template.render(request=request))

def create_user(request):
    """view called when a user on the login page try to create a new
    registered user"""

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
    """view called when a user try to login on the login page"""

    if request.method == 'POST':
        login_username = request.POST.get('login_username')
        login_password = request.POST.get('login_password')
        if login_username and login_password:
            if User.objects.filter(username=login_username).exists():
                user = authenticate(username=login_username,
                                    password=login_password)
                if user is not None:
                    login(request, user)
                    picture_exist = Profil.objects.filter(user=request.user.id)
                    if picture_exist.exists():
                        picture_exist = Profil.objects.get(user=request.user.id)
                        picture = picture_exist.image_url
                        regex = re.compile("http:")
                        if regex.match(picture) == None:
                            picture = False
                    else:
                        picture = False
                    context = {"user_name": request.user.username,
                               "user_email": request.user.email,
                               "picture": picture}
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
    """view called when a logged user save a new favorite"""

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
    """view called when a user want to see the page of a product"""

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
    """view called when a logged user wants to see his favorite"""

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
    """view called when a user wants to log out (a visitor will just be
    redirected to the index)"""

    logout(request)
    template = loader.get_template('product/index.html')
    return HttpResponse(template.render(request=request))

def legal_notice(request):
    """view called when the user wants to see the legal notice page"""

    template = loader.get_template('product/legalnotice.html')
    return HttpResponse(template.render(request=request))

def delete(request):
    """view called when a user wants to delete a favorite previously
    registered"""

    del_mess = False
    if request.method == 'POST':
        product_to_delete = request.POST.get('product_id')
        product_obj = Product(id=product_to_delete)
        product_obj.user.remove(request.user.id)
        del_mess = True
    products = Product.objects.filter(user=request.user.id).order_by('id')
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)
    context = {"products": product, "paginate": True, "del_mess": del_mess}
    template = loader.get_template('product/myproduct.html')
    return HttpResponse(template.render(context, request=request))

def change_username(request):
    """view called if a user wants to change his username"""

    if request.method == 'POST':
        new_username = request.POST.get('change_username')
        password = request.POST.get('password')
        if new_username and check_password(password, request.user.password):
            if User.objects.filter(username=new_username).exists():
                context = {"change": "Ce pseudo est déjà utilisé.",
                           "user_name": request.user.username,
                           "user_email": request.user.email}
                template = loader.get_template('product/user.html')
                return HttpResponse(template.render(context, request=request))
            else:
                user = User.objects.get(username=request.user.username)
                user.username = new_username
                user.save()
                logout(request)
                context = {"created":
                           "Pseudo modifié! Veuillez vous reconnecter",
                          }
                template = loader.get_template('product/login.html')
                return HttpResponse(template.render(context, request=request))
        else:
            context = {"change": "Remplissez tous les champs.",
                       "user_name": request.user.username,
                       "user_email": request.user.email}
            template = loader.get_template('product/user.html')
            return HttpResponse(template.render(context, request=request))
    else:
        context = {"user_name": request.user.username,
                   "user_email": request.user.email}
        template = loader.get_template('product/user.html')
        return HttpResponse(template.render(context, request=request))

def change_password(request):
    """view called if a user wants to change his password"""

    if request.method == 'POST':
        new_password = request.POST.get('change_password')
        new_password_check = request.POST.get('new_password')
        old_password = request.POST.get('old_password')
        if new_password and new_password_check and\
           (new_password == new_password_check) and\
           check_password(old_password, request.user.password):
            user = User.objects.get(username=request.user.username)
            print(user.username)
            user.set_password(new_password)
            user.save()
            logout(request)
            context = {"created":
                       "Mot de passe modifié! Veuillez vous reconnecter"
                      }
            template = loader.get_template('product/login.html')
            return HttpResponse(template.render(context, request=request))
        else:
            context = {"change": "Remplissez tous les champs.",
                       "user_name": request.user.username,
                       "user_email": request.user.email}
            template = loader.get_template('product/user.html')
            return HttpResponse(template.render(context, request=request))
    else:
        context = {"user_name": request.user.username,
                   "user_email": request.user.email}
        template = loader.get_template('product/user.html')
        return HttpResponse(template.render(context, request=request))

def change_email(request):
    """view called if a user wants to change his email"""

    if request.method == 'POST':
        new_email = request.POST.get('change_email')
        password = request.POST.get('password')
        if new_email and check_password(password, request.user.password):
            if User.objects.filter(email=new_email).exists():
                context = {"change": "Cet email est déjà utilisé.",
                           "user_name": request.user.username,
                           "user_email": request.user.email}
                template = loader.get_template('product/user.html')
                return HttpResponse(template.render(context, request=request))
            else:
                user = User.objects.get(username=request.user.username)
                user.email = new_email
                user.save()
                logout(request)
                context = {"created":
                           "Email modifié! Veuillez vous reconnecter"
                          }
                template = loader.get_template('product/login.html')
                return HttpResponse(template.render(context, request=request))
        else:
            context = {"change": "Remplissez tous les champs.",
                       "user_name": request.user.username,
                       "user_email": request.user.email}
            template = loader.get_template('product/user.html')
            return HttpResponse(template.render(context, request=request))
    else:
        context = {"user_name": request.user.username,
                   "user_email": request.user.email}
        template = loader.get_template('product/user.html')
        return HttpResponse(template.render(context, request=request))

def change_picture(request):
    """view called if a user wants to change his picture profil"""

    if request.method == 'POST':
        picture_url = request.POST.get('picture_url')
        if picture_url:
            picture_exist = Profil.objects.filter(user=request.user.id)
            if picture_exist.exists():
                picture_exist = Profil.objects.get(user=request.user.id)
                picture_exist.image_url = picture_url
                picture_exist.save()
            else:
                new_picture = Profil(image_url=picture_url, user=request.user)
                new_picture.save()
            regex = re.compile("http:")
            if regex.match(picture_url) == None:
                picture_url = False
            context = {"user_name": request.user.username,
                       "user_email": request.user.email,
                       "picture": picture_url}
            template = loader.get_template('product/user.html')
            return HttpResponse(template.render(context, request=request))
    picture_exist = Profil.objects.filter(user=request.user.id)
    if picture_exist.exists():
        picture_exist = Profil.objects.get(user=request.user.id)
        picture = picture_exist.image_url
        regex = re.compile("http:")
        if regex.match(picture) == None:
            picture = False
    else:
        picture = False
    context = {"user_name": request.user.username,
               "user_email": request.user.email,
               "picture": picture}
    template = loader.get_template('product/user.html')
    return HttpResponse(template.render(context, request=request))
