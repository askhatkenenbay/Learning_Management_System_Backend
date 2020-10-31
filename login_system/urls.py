from django.urls import path, include
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.login, name='login'),
    path('reg/', views.reg, name='reg'),
    path('article',views.art, name='art'),
    path('article/1',views.artOne, name='artOne'),
    path('article/2',views.artTwo, name='artTwo'),
    path('article/3',views.artThree, name='artThree'),
    path('challenges/', include('challenges.urls')),
]
