from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Product

class StatusCodeTestCase(TestCase):
    """Test if the views that must return a status_code 200 return that
    status_code"""

    def test_index_page(self):
        """Test if the '' path return the index page"""

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_page_methodetwo(self):
        """Test if the 'index/' path return the index page"""

        response = self.client.get(reverse('index_two'))
        self.assertEqual(response.status_code, 200)

    def test_legalnotice_page(self):
        """Test if the 'legal_notice' path return the legal notice page"""

        response = self.client.get(reverse('legal_notice'))
        self.assertEqual(response.status_code, 200)

    def test_save_toindex(self):
        """Test if the 'save' path return the index page if no post methode"""

        response = self.client.get(reverse('save'))
        self.assertEqual(response.status_code, 200)

    def test_connect_toindex(self):
        """Test if the 'connect_user' path return the index page if no post
        methode"""

        response = self.client.get(reverse('connect_user'))
        self.assertEqual(response.status_code, 200)

    def test_create_user_toindex(self):
        """Test if the 'create_user' path return the index page if no post
        methode"""

        response = self.client.get(reverse('create_user'))
        self.assertEqual(response.status_code, 200)

class UserTestCase(TestCase):
    """User related testing class"""

    def setUp(self):

        self.user = User.objects.create_user(
            email='test@b.com', username='testb', password='0000')

    def test_create_user_page(self):
        """Test the user creation view"""

        response = self.client.post(reverse('create_user'), data={
            'create_email':'test@a.com',
            'create_username':'testa',
            'create_password':'0000'
            })
        self.assertEqual(response.context['created'],
                         "Votre compte a été crée, connectez vous!")

    def test_create_user_fail(self):
        """Test the fail creation condition in the creat user view"""

        response = self.client.post(reverse('create_user'), data={
            'create_email':'test@a.com',
            'create_username':'testa',
            })
        self.assertEqual(response.context['errorc'],
                         "Remplissez tous les champs.")
        response = self.client.post(reverse('create_user'), data={
            'create_email':'test@b.com',
            'create_username':'testa',
            'create_password':'0000'
            })
        self.assertEqual(response.context['errorc'],
                         "Cet email est déjà utilisé.")
        response = self.client.post(reverse('create_user'), data={
            'create_email':'test@a.com',
            'create_username':'testb',
            'create_password':'0000'
            })
        self.assertEqual(response.context['errorc'],
                         "Ce pseudo est déjà utilisé.")

    def test_user_page_connected(self):
        """Test if the user can go to his user page when connected"""

        self.client.login(username='testb', password='0000')
        response = self.client.get(reverse('user_page'))
        self.assertEqual(response.context['user_name'], 'testb')

    def test_user_page_notconnected(self):
        """Test if a visitor can't go to the user page"""

        response = self.client.get(reverse('user_page'))
        try:
            user_name = response.context['user_name']
        except:
            user_name = False
        self.assertEqual(user_name, False)

    def test_connect_user_page(self):
        """Test the user connection view"""

        response = self.client.post(reverse('connect_user'), data={
            'login_username':'testb',
            'login_password':'0000'
            })
        self.assertEqual(response.context['user'].is_authenticated, True)

    def test_connect_user_fail(self):
        """Test the fail connection condition in the connect user view"""

        response = self.client.post(reverse('connect_user'), data={
            'login_username':'testc',
            'login_password':'0000'
            })
        self.assertEqual(response.context['errorl'],
                         "L'utilisateur n'existe pas.")
        response = self.client.post(reverse('connect_user'), data={
            'login_password':'0000'
            })
        self.assertEqual(response.context['errorl'],
                         "Remplissez tous les champs.")
        response = self.client.post(reverse('connect_user'), data={
            'login_username':'testb',
            'login_password':'0001'
            })
        self.assertEqual(response.context['errorl'],
                         "Le mot de passe est incorrect.")

    def test_logout_page(self):
        """Test the logout connection view"""

        self.client.login(username='testb', password='0000')
        response = self.client.get(reverse('user_logout'))
        self.assertEqual(response.context['user'].is_authenticated, False)

class ProductTestCase(TestCase):
    """Product related testing class"""

    def setUp(self):

        Category.objects.create(
            name='pizzas')
        Product.objects.create(
            name='dolce regina',
            nutrition_grades='c',
            ingredients='jambon, tomates',
            url='https://www.quelquepart.com',
            image_url='https://www.plusloin.com',
            category_id='1')
        Product.objects.create(
            name='raviolis pizza',
            nutrition_grades='c',
            ingredients='boeuf, tomates',
            url='https://www.quelquepart2.com',
            image_url='https://www.plusloin2.com',
            category_id='1')
        self.product = Product.objects.get(name='dolce regina')
        self.user = User.objects.create_user(
            email='test@b.com', username='testb', password='0000')

    def test_product_pages(self):
        """Test the views that record and retrievs links between user and
        products. Test also the product searching view"""

        response = self.client.post(reverse('search'), data={
            'query':'dolce', 'category':'1'})
        for products in response.context["products"]:
            if products.name == "dolce regina":
                search_result = "dolce regina"
        self.assertEqual(search_result, self.product.name)
        response = self.client.get(reverse('product_page', args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.client.login(username='testb', password='0000')
        response = self.client.post(reverse('save'), data={
            'product_id':1})
        products = Product.objects.filter(user=response.context['user'].id)
        test = "bad"
        for product in products:
            if product.id == 1:
                test = "ok"
        self.assertEqual(test, "ok")
        response = self.client.get(reverse('user_product'))
        products = response.context['products']
        for product in products:
            if product.id == 1:
                test = "ok"
        self.assertEqual(test, "ok")
