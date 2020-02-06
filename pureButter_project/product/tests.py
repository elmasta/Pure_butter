from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Product, Profil

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

    def test_user_page_connected_withpic(self):
        """Test if the user which has a profil picture can go to his user page
        when connected"""

        self.client.login(username='testb', password='0000')
        Profil.objects.create(
            image_url='http://www.lololololol.com',
            user=self.user)
        response = self.client.get(reverse('user_page'))
        self.assertEqual(response.context['picture'],
                         'http://www.lololololol.com')

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

    def test_connect_user_page_withpic(self):
        """Test the user connection view if the user has a profil picture"""

        Profil.objects.create(
            image_url='http://www.lololololol.com',
            user=self.user)
        response = self.client.post(reverse('connect_user'), data={
            'login_username':'testb',
            'login_password':'0000'
            })
        self.assertEqual(response.context['picture'],
                         'http://www.lololololol.com')

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

    def test_changeusername_page(self):
        """Test the change username view"""

        self.client.login(username='testb', password='0000')
        #also test if the page is reloaded if there's no post method.
        response = self.client.get(reverse('change_username'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('change_username'), data={
            'change_username':'testb',
            'password':'0000'
            })
        self.assertEqual(response.context['change'],
                         "Ce pseudo est déjà utilisé.")
        response = self.client.post(reverse('change_username'), data={
            'change_username':'testb'
            })
        self.assertEqual(response.context['change'],
                         "Remplissez tous les champs.")
        response = self.client.post(reverse('change_username'), data={
            'change_username':'testz',
            'password':'0000'
            })
        self.assertEqual(response.context['created'],
                         "Pseudo modifié! Veuillez vous reconnecter")

    def test_changepassword_page(self):
        """Test the change password view"""

        self.client.login(username='testb', password='0000')
        #also test if the page is reloaded if there's no post method.
        response = self.client.get(reverse('change_password'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('change_password'), data={
            'change_password':'testb'
            })
        self.assertEqual(response.context['change'],
                         "Remplissez tous les champs.")
        response = self.client.post(reverse('change_password'), data={
            'change_password':'4444',
            'new_password':'4444',
            'old_password':'0000'
            })
        self.assertEqual(response.context['created'],
                         "Mot de passe modifié! Veuillez vous reconnecter")

    def test_changeemail_page(self):
        """Test the change email view"""

        self.client.login(username='testb', password='0000')
        #also test if the page is reloaded if there's no post method.
        response = self.client.get(reverse('change_email'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('change_email'), data={
            'change_email':'test@b.com',
            'password':'0000'
            })
        self.assertEqual(response.context['change'],
                         "Cet email est déjà utilisé.")
        response = self.client.post(reverse('change_email'), data={
            'change_email':'testb@g.com'
            })
        self.assertEqual(response.context['change'],
                         "Remplissez tous les champs.")
        response = self.client.post(reverse('change_email'), data={
            'change_email':'test@z.com',
            'password':'0000'
            })
        self.assertEqual(response.context['created'],
                         "Email modifié! Veuillez vous reconnecter")

    def test_changepicture_page(self):
        """Test the change picture view"""

        self.client.login(username='testb', password='0000')
        response = self.client.get(reverse('change_picture'))
        self.assertEqual(response.context['picture'], False)
        Profil.objects.create(
            image_url='http://www.lololololol.com',
            user=self.user)
        response = self.client.get(reverse('change_picture'))
        self.assertEqual(response.context['picture'],
                         'http://www.lololololol.com')
        response = self.client.post(reverse('change_picture'), data={
            'picture_url':'http://www.lalalalala.com'
            })
        picture_test = Profil.objects.get(user=self.user)
        self.assertEqual(response.context['picture'],
                         picture_test.image_url)

    def test_changepicture_new(self):
        """Test the change picture view if the user had no picture before"""

        self.client.login(username='testb', password='0000')
        response = self.client.post(reverse('change_picture'), data={
            'picture_url':'http://www.lalalalala.com'
            })
        picture_test = Profil.objects.get(user=self.user)
        self.assertEqual(response.context['picture'],
                         picture_test.image_url)

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

        #the next 3 assert are search test
        response = self.client.post(reverse('search'), data={'category':'1'})
        for products in response.context["products"]:
            if products.name == "dolce regina":
                search_result = "dolce regina"
        self.assertEqual(search_result, self.product.name)

        response = self.client.post(reverse('search'), data={
            'query':'dolce', 'category':'1'})
        for products in response.context["products"]:
            if products.name == "dolce regina":
                search_result = "dolce regina"
        self.assertEqual(search_result, self.product.name)

        response = self.client.get(reverse('search'))
        for products in response.context["products"]:
            if products.name == "dolce regina":
                search_result = "dolce regina"
        self.assertEqual(search_result, self.product.name)

        #test if product page return 200
        response = self.client.get(reverse('product_page', args=(1,)))
        self.assertEqual(response.status_code, 200)

        #test if a favorite is saved in database
        self.client.login(username='testb', password='0000')
        response = self.client.post(reverse('save'), data={
            'product_id':1})
        products = Product.objects.filter(user=response.context['user'].id)
        test = "bad"
        for product in products:
            if product.id == 1:
                test = "ok"
        self.assertEqual(test, "ok")

        #test if a product saved appear on the user product page
        response = self.client.get(reverse('user_product'))
        products = response.context['products']
        for product in products:
            if product.id == 1:
                test = "ok"
        self.assertEqual(test, "ok")

        #test if a product saved doesn't appear in new search
        response = self.client.post(reverse('search'), data={'category':'1'})
        test = "ok"
        for products in response.context["products"]:
            if products.name == "dolce regina":
                test = "bad"
        self.assertEqual(test, "ok")

        #test if product page return 200 even without post method or favorite
        #deletion
        #view's named "delete" but path's named "del"
        response = self.client.get(reverse('del'))
        self.assertEqual(response.context['del_mess'], False)

        #test the favorite deletion
        response = self.client.post(reverse('del'), data={
            'product_id':1})
        test = "ok"
        products = Product.objects.filter(user=response.context['user'].id)
        for product in products:
            if product.id == 1:
                test = "bad"
        self.assertEqual(test, "ok")
