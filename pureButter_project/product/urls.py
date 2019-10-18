from django.urls import path
from . import views

urlpatterns = [
    path('results/', views.search, name='search'),
    path('user/', views.user_page),
    path('user/user_created', views.create_user, name='create_user'),
    path('user/failed_connect_user', views.connect_user, name='connect_user'),
    path('user/logout', views.user_logout, name='user_logout'),
    path('product', views.save, name='save')
]
