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
from manager_site.forms import EditEmployee
from django.contrib.auth.views import LoginView,TemplateView
from manager_site import views
from manager_site.views import ProductView,SupplierView,SalesView,LogView,EmployeeView,ProfileView,home_detail_view,manager_home_view,manager_emp_view,manager_signin_view,manager_supplier_view,manager_supplier_modify_view,manager_stock_view,manager_stock_modify_view,manager_finance_view,manager_record_view,manager_wagecal_view,showform,logform,logactive
from employee_site.views import employee_sales_view,employee_viewall_view
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
    path('manager-home/',manager_home_view),
    path('manager-home/employee-management/list',EmployeeView),
    path('manager-home/employee-management/addrem',showform),
    path('manager-home/employee-management/mod',views.edit_employee),
    path('manager-home/employee-management/',manager_emp_view),
    path('log/',logform),
    path('manager-home/supplier-management/',manager_supplier_view),
    path('manager-home/supplier-management/modify/',manager_supplier_modify_view),
    path('manager-home/stock-management/',manager_stock_view),
    path('manager-home/stock-management/modify/',manager_stock_modify_view),
    path('manager-home/finance/',manager_finance_view),
    path('manager-home/record/',manager_record_view),
    path('employee-home/sales/',employee_sales_view),
    path('employee-home/sales/view/',employee_viewall_view),
    path('manager-home/wage-calculation/', manager_wagecal_view),
    path('log/active/', logactive),
]
