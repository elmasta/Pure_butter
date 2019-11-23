from django.urls import path
from . import views

urlpatterns = [
    path('results/', views.search, name='search'),
    path('user/', views.user_page, name='user_page'),
    path('user/user_created', views.create_user, name='create_user'),
    path('user/connect', views.connect_user, name='connect_user'),
    path('user/logout', views.user_logout, name='user_logout'),
    path('product_info', views.save, name='save'),
    path('info/<product_id>', views.product_page, name='product_page'),
    path('user_product', views.user_product, name='user_product'),
    path('legal_notice', views.legal_notice, name='legal_notice')
]
