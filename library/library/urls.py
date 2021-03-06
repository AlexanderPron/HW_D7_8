"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from catalog import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from catalog.views import ShowUserProfile, CreateUserProfile
from django.urls import reverse_lazy
from allauth.account.views import login, logout, signup
from django.conf.urls import url

urlpatterns = [
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('book_increment/', views.book_increment),
    path('book_decrement/', views.book_decrement),
    path('ph/', views.ph, name='ph'),
    path('bk/', views.bk, name='bk'),
    path('add/', views.book_add, name='add-book'),
    path('login/', login, name='login'),  
    path('logout/', logout, name='logout'),
    path('register/', signup, name='register'),
    path('profile/<int:pk>/add', CreateUserProfile.as_view(), name='profile-add'),
    path('profile/<int:pk>', ShowUserProfile.as_view(), name='profile-show'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)