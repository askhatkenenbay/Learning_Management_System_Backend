from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.login, name='login'),
    path('reg/', views.reg, name='reg'),
    path('article',views.art, name='art'),
    path('article/1',views.artOne, name='artOne'),
]
