"""dbms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib.auth.views import LoginView,TemplateView
from manager_site.views import ProductView,SupplierView,SalesView,LogView,ProfileView,home_detail_view,manager_home_view,manager_emp_view,manager_signin_view

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('',LoginView.as_view(template_name="registration/login.html")),
   #path('accounts/profile/',ProfileView.as_view(template_name="base.html")),
    path('manager-home/products',ProductView.as_view(template_name="products.html")),
    #path('accounts/profile/sales',SalesView.as_view(template_name="sales.html")),
    path('manager-home/supplier',SupplierView.as_view(template_name="supplier.html")),
    #path('accounts/profile/log',LogView.as_view(template_name="log.html")),
    path('',home_detail_view ),
    path('manager-signin/',manager_signin_view ),
    path('manager-home/',ProfileView.as_view(template_name="base.html")),
    path('manager-home/employee-management/',ProductView.as_view(template_name="manager_emp.html")),
]
