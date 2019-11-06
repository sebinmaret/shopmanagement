from django.shortcuts import render,redirect
from django.contrib.auth import authenticate


# Create your views here.
from django.shortcuts import render, redirect
from django.views.generic import TemplateView,ListView
from django.contrib.auth import authenticate
# Create your views here.
from Shop.models import SalesRecord,Supplier,Products,ExpiryDetails,SupplierCat

class ProductView(TemplateView):
    template_name = "templates/manager_emp.html"

    def get(self,request):
        object_list = Products.objects.raw('select * from Shop_products')
        args = {'object_list':object_list}
        return render(request,self.template_name,args)


def home_detail_view(request):
	return render(request,"registration/detail.html",{})

class ProfileView(TemplateView):
    template_name="templates/registration/base.html"
    


class SalesView(TemplateView):
    template_name = "templates/sales.html"

    def get(self,request):
        object_list = Supplier.objects.raw('select * from Shop_salesrecord')
        args = {'object_list':object_list}
        return render(request,self.template_name,args)

class SupplierView(TemplateView):
    template_name = "templates/supplier.html"

    def get(self,request):
        object_list = Supplier.objects.raw('select * from Shop_supplier')
        args = {'object_list':object_list}
        return render(request,self.template_name,args)

class LogView(TemplateView):
    template_name = "templates/log.html"

    def get(self,request):
        object_list = Supplier.objects.raw('select * from Shop_logrecord')
        args = {'object_list':object_list}
        return render(request,self.template_name,args)

def manager_signin_view(request):
	if request.method =="POST":
		username_inp=request.POST.get('uname')
		pass_inp=request.POST.get('psw')
		user = authenticate(username=username_inp,password=pass_inp)
		if user is not None:
			return redirect("http://127.0.0.1:8000/manager-home/")

	return render(request,"manager_signin.html",{})


def manager_home_view(request):
	return render(request,"manager_home.html",{})



def manager_emp_view(request):
	return render(request,"manager_emp.html",{})