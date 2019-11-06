from django.shortcuts import render, redirect
from django.views.generic import TemplateView,ListView
from django.contrib.auth import authenticate
# Create your views here.
from Shop.models import SalesRecord,Supplier,Products,ExpiryDetails,SupplierCat

