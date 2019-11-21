from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate
from django.db import connection,transaction
from datetime import datetime,date
from django.contrib import messages
from .forms import AddEmployee,EditEmployee
from django.template import RequestContext
from django.views.generic import TemplateView,ListView
from django.http import HttpResponse
# Create your views here.
from Shop.models import SalesRecord,Supplier,Products,ExpiryDetails,SupplierCat,LogRecord, Employee

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
    if request.method =="POST" :
        username_inp=request.POST.get('uname')
        pass_inp=request.POST.get('psw')
        user = authenticate(username=username_inp,password=pass_inp)
        if user is  not None:
            return redirect("/manager-home/")
        else:
            obj={
                'error1':1
            }
            return render(request,"manager_signin.html",obj)
    return render(request,"manager_signin.html",{})

def manager_home_view(request):
	return render(request,"base.html",{})

def manager_supplier_view(request):
    print(request.method)
    obj={
        'enter':0,
        'test': "*"
    }
    if request.method=="POST":
        cat=request.POST.get('category')
        cat=cat.title()
        print (cat)
        if(cat == "*"):
            x=Supplier.objects.raw(" SELECT DISTINCT * FROM Shop_supplier JOIN  Shop_suppliercat ON Shop_supplier.s_id = Shop_suppliercat.s_id_id") 
        else:   
            x=Supplier.objects.raw(" SELECT DISTINCT * FROM Shop_supplier JOIN  Shop_suppliercat ON Shop_supplier.s_id = Shop_suppliercat.s_id_id WHERE Shop_suppliercat.category = %s",[cat]) 
        for y in x:
            print(y.category)
        obj={
          'table':x,
          'enter':1,
          'test':cat
        }
        return render(request,"supplier-management.html",obj)
    return render(request,"supplier-management.html",obj)

def manager_supplier_modify_view(request):
    if request.method=="POST":
        sidrem=request.POST.get('s_id_rem')
        if(sidrem is None):
            cat=request.POST.get('category')
            cat=cat.title()
            cat=cat.split(",")
            add=request.POST.get('add')
            add=add.title()
            sid=request.POST.get('s_id')
            sid=int(sid)
            cno=request.POST.get('contact_no')
            cno=int(cno)
            sname=request.POST.get('name')
            sname=sname.title()
            temp=Supplier.objects.raw("SELECT * FROM Shop_supplier WHERE Shop_supplier.s_id = %s",[sid])
            if(len(temp)>0):
                obj={
                    'error1':1
                }
                return render(request,"manager_supplier_modify.html",obj)        
            c=connection.cursor()
            c.execute('INSERT INTO Shop_supplier VALUES (%s,%s,%s,%s)',[sid,add,cno,sname])
            x=SupplierCat.objects.raw("SELECT * FROM Shop_suppliercat GROUP BY Shop_suppliercat.s_id_id ")
            max1=0

            for y in x:
                if(y.id is not None and y.id != ""):
                    if(max1<y.id):
                        max1=y.id
            max1=max1+1
          
            for i in cat:
                if i:
                    i=i.strip()
                    print(i)
                    c.execute('INSERT INTO Shop_suppliercat VALUES (%s,%s,%s)',[max1,i,sid])
                    max1=max1+1
            obj={
                'success1':1
            }
        else:
            temp=Supplier.objects.raw("SELECT * FROM Shop_supplier WHERE Shop_supplier.s_id = %s",[sidrem])
            if(len(temp)==0):
                obj={
                    'error2':1
                }
                return render(request,"manager_supplier_modify.html",obj)
            temp=Products.objects.raw("SELECT * FROM Shop_products WHERE Shop_products.s_id_id = %s",[sidrem])
            c=connection.cursor()
            c.execute('DELETE FROM Shop_suppliercat WHERE Shop_suppliercat.s_id_id = %s',[sidrem])
            r=0
            for y in temp:
                c.execute('DELETE FROM Shop_expirydetails WHERE Shop_expirydetails.p_id_id = %s',[y.p_id])
            c.execute('DELETE FROM Shop_products WHERE Shop_products.s_id_id = %s',[sidrem])
            r=10
            c.execute('DELETE FROM Shop_supplier WHERE Shop_supplier.s_id = %s',[sidrem])
            obj={
                'success2':1
            }
#        x=Supplier.objects.raw("INSERT INTO Shop_supplier VALUES  (%d,%s,%d,%s) ",[sid,add,cno,sname])
        return render(request,"manager_supplier_modify.html",obj)    
    return render(request,"manager_supplier_modify.html",{})


def manager_stock_view(request):
    print(request.method)
    if request.method=="POST":
        cat=request.POST.get('category')
        cat=cat.title()
        print (cat)
        if(cat == "*"):
            x=Products.objects.raw(" SELECT Shop_products.p_id, Shop_products.price, Shop_products.typE, Shop_products.company, Shop_products.category, Shop_products.s_id_id, Shop_expirydetails.quantity AS expqty ,Shop_products.quantity, Shop_expirydetails.date FROM Shop_products LEFT JOIN Shop_ExpiryDetails ON Shop_Products.p_id = Shop_ExpiryDetails.p_id_id ORDER BY Shop_Products.p_id , Shop_Products.category , Shop_ExpiryDetails.date") 
        else:   
            x=Products.objects.raw(" SELECT Shop_products.p_id, Shop_products.price, Shop_products.typE, Shop_products.company, Shop_products.category, Shop_products.s_id_id, Shop_expirydetails.quantity AS expqty ,Shop_products.quantity, Shop_expirydetails.date FROM Shop_products LEFT JOIN Shop_ExpiryDetails ON Shop_Products.p_id = Shop_ExpiryDetails.p_id_id WHERE Shop_products.category = %s ORDER BY Shop_Products.p_id , Shop_Products.category , Shop_ExpiryDetails.date",[cat]) 
        for j in x:
            print(vars(j))

        obj={
          'table':x
        }
        return render(request,"stock-management.html",obj)
    return render(request,"stock-management.html",{})  

    
def manager_stock_modify_view(request):
    if request.method=="POST":
        pid1=request.POST.get('p_id1')
        if pid1 is not None:
            price1=request.POST.get('price1')
            qty1=request.POST.get('qty1')
            type1=request.POST.get('typE1')
            type1=type1.title()
            cat1=request.POST.get('cat1')
            cat1=cat1.title()
            company1=request.POST.get('comp1')
            company1=company1.title()
            sid1=request.POST.get('s_id1')
            exp1=request.POST.get('exp1')
            temp=Products.objects.raw("SELECT * FROM Shop_products WHERE Shop_products.p_id = %s",[pid1])
            if(len(temp)>0):
                obj={
                    'error2':1
                }                
                return render(request,"manager_stock_modify.html",obj)
            print(company1)
            c=connection.cursor()
            c.execute('INSERT INTO Shop_products VALUES (%s,%s,%s,%s,%s,%s,%s) ',[pid1,qty1,price1,company1,cat1,sid1,type1])
            print("-----")
            print(type(exp1),len(exp1))
            if (exp1 is not None) and (exp1 != ""):
                x=ExpiryDetails.objects.raw(" SELECT * ,count(*) AS count FROM  Shop_expirydetails ") 
                max1=0
                for y in x:
                    if (y.id is  not None) and (max1<y.id):
                        max1=y.id
                y=max1+1
                c.execute('INSERT INTO Shop_expirydetails VALUES (%s,%s,%s,%s) ',[y,exp1,pid1,qty1])
            obj={
                'success1':1
            }
            return render(request,"manager_stock_modify.html",obj) 
        else:
            pid=request.POST.get('p_id')
            qty=request.POST.get('qty')
            date1=request.POST.get('date')
            temp=Products.objects.raw("SELECT * FROM Shop_products WHERE Shop_products.p_id = %s",[pid])
            if(len(temp)==0):
                obj={
                    'error1':1
                }                
                return render(request,"manager_stock_modify.html",obj) 
            c=connection.cursor()
            c.execute('UPDATE Shop_products SET quantity = quantity + %s WHERE p_id = %s',[qty,pid])
            transaction.commit()
            print("----")
            print(date1)
            if(date1 is None ) or (date1==""):
                obj={
                'success2':1
                }
                return render(request,"manager_stock_modify.html",obj)
            x=ExpiryDetails.objects.raw(" SELECT * ,count(*) AS count FROM  Shop_expirydetails ") 
            max1=0
            for y in x:
                if(y.id is not None and max1<y.id):
                    max1=y.id

            #date=str(date)
            #date=datetime.datetime.strptime(date,'%Y-%m-%d').date()
            y=max1+1
            print(date)
            pid=int(pid)
            qty=int(qty)
            c.execute('INSERT INTO Shop_expirydetails VALUES (%s,%s,%s,%s) ',[y,date1,pid,qty])
            obj={
                'success2':1
            }
            return render(request,"manager_stock_modify.html",obj) 
    return render(request,"manager_stock_modify.html",{})

def manager_finance_view(request):
    if request.method=="POST":
        sdate=request.POST.get('sdate')
        if sdate is not None:
            sdate=parsedate1(sdate)
            edate=parsedate1(request.POST.get('edate'))
            x=SalesRecord.objects.raw(" SELECT Shop_salesrecord.r_id,Shop_salesrecord.date,Shop_salesrecord.total_price FROM Shop_salesrecord ") 
            totalrev=0
            print(dir(x))
            for y in x:
                date1=y.date
                date1=parsedate1(date1)
                if (date1<=edate and date1>=sdate):
                    totalrev=totalrev+y.total_price
            obj={
                'value': totalrev,
                'sdate1':sdate.date(),
                'edate1':edate.date()
            }
            return render(request,"manager_finances.html",obj) 
        else:
            sdate_in=parsedate1(request.POST.get('sdate1'))
            edate_in=parsedate1(request.POST.get('edate1'))

            x=LogRecord.objects.raw(" SELECT * FROM Shop_logrecord ")

            total=0
            for i in x:
                date1=parsedate1(i.date)
                if date1 >= sdate_in and date1 <=edate_in:
                    z=Employee.objects.raw(" SELECT * FROM Shop_employee WHERE Shop_employee.e_id = %s",[i.e_id.e_id])

                    for j in z:
                        wage=j.wage
                        start=parsetime1(i.sign_in)
                        end=parsetime1(i.sign_out)

                        work_hrs=((end-start).seconds)/3600
                        total= total + (work_hrs *wage)

            obj={
                'value1':total,
                'sdate1':sdate_in.date(),
                'edate1':edate_in.date()
            }
            return render(request,"manager_finances.html",obj) 

    return render(request,"manager_finances.html",{}) 


def parsedate1(input12):
    input12=input12.split("-")
    for i in input12:
        i=i.strip()
    year=int(input12[0])
    month=int(input12[1])
    day=int(input12[2])
    try:
        retdate=datetime(year,month,day)
    except ValueError:
        return None
    return retdate

def manager_record_view(request):
    if request.method=="POST":
        sdate=request.POST.get('sdate')
        if sdate is not None:
            sdate=parsedate1(sdate)
            edate=parsedate1(request.POST.get('edate'))
            x=SalesRecord.objects.raw(" SELECT * FROM Shop_salesrecord ") 
            for y in x:
                print(y.date)
                y.date=parsedate1(y.date)

            obj={
                'value': 1,
                'object': x,
                'startdate': sdate,
                'enddate': edate
            }
            return render(request,"manager_record.html",obj) 
        else:
            sdate1=parsedate1(request.POST.get('sdate1'))
            edate1=parsedate1(request.POST.get('edate1'))
            x=LogRecord.objects.raw(" SELECT * FROM Shop_logrecord") 

            for y in x:
                if y.date is not None:
                    y.date=parsedate1(y.date)
                    #print(y.date)
            obj={
                'value1': 1,
                'object': x,
                'startdate': sdate1,
                'enddate': edate1
            }
            return render(request,"manager_record.html",obj) 


    return render(request,"manager_record.html",{})

def manager_wagecal_view(request):
    obj={}
    if request.method=="POST":
        eid=request.POST.get('e_id')
        eid2=eid
        sdate=parsedate1(request.POST.get('sdate'))
        edate=parsedate1(request.POST.get('edate'))

        x= LogRecord.objects.raw(" SELECT * FROM Shop_logrecord WHERE e_id_id=%s", [eid])
        z= Employee.objects.raw(" SELECT * FROM Shop_employee WHERE e_id=%s",[eid])
        if(len(z)==0):
            obj={
                'error1':1
            }
            return render(request,"manager_wagecal.html",obj)               
        for i in z:
            wage=i.wage
        sum1=0
        total_wrk_hrs=0
        for i in x:

            if parsedate1(i.date) >= sdate and parsedate1(i.date) <=edate:
                start=parsetime1(i.sign_in)
                end=parsetime1(i.sign_out)

                work_hrs=((end-start).seconds)/3600
                total_wrk_hrs=total_wrk_hrs+work_hrs
                sum1=sum1 + work_hrs * wage
        obj={
            'value':sum1,
            'empid':eid2,
            'sdate1':sdate.date(),
            'edate1':edate.date(),
            'total_hrs':total_wrk_hrs
        }

    return render(request,"manager_wagecal.html",obj)   

def parsetime1(input12):
    input12=input12.split(':')

    hr=int(input12[0])
    mins=int(input12[1])

    rettime=datetime(2000,1,24,hr,mins)
    return rettime

#---------------------------------------------------------------------------
def manager_emp_view(request):
    return render(request,"manager_emp.html",{})

def EmployeeView(request):
    print(request.method)
    obj={
        'enter':0,
        'test':0
    }
  

    if request.method=="POST":
        eid=request.POST.get('eid')
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        wage=request.POST.get('wage')
        address=request.POST.get('address')
        print(fname)
        print (eid)
        if(eid == '0'):
            print("HI ALL")
            x=Employee.objects.raw(" SELECT  * FROM Shop_employee") 
        elif(eid!=''):   
            x=Employee.objects.raw(" SELECT  * FROM Shop_employee WHERE Shop_employee.e_id = %s",[eid]) 

        if(fname == '0'):
            print("HI ALL")
            x=Employee.objects.raw(" SELECT  * FROM Shop_employee") 
        elif(fname != ''):   
            x=Employee.objects.raw(" SELECT  * FROM Shop_employee WHERE Shop_employee.f_name = %s",[fname]) 


        if(lname == '0'):
            print("HI ALL")
            x=Employee.objects.raw(" SELECT  * FROM Shop_employee") 
        elif(lname!=''):   
            x=Employee.objects.raw(" SELECT  * FROM Shop_employee WHERE Shop_employee.l_name = %s",[lname]) 

        if(wage == '0'):
            print("HI ALL")
            x=Employee.objects.raw(" SELECT  * FROM Shop_employee") 
        elif(wage!=''):   
            x=Employee.objects.raw(" SELECT  * FROM Shop_employee WHERE Shop_employee.wage = %s",[wage])
        '''
        if(address == '0'):
            print("HI ALL")
            x=Employee.objects.raw(" SELECT  * FROM Shop_employee") 
        elif(address!=''):   
            x=Employee.objects.raw(" SELECT  * FROM Shop_employee WHERE Shop_employee.address like '%% %s %%' ",[address])
        #for y in x:
         #   print(y.category)
        '''
        obj={
        'table':x,
        'enter':1,
        'test':eid
        }
        return render(request,"emp-management/list.html",obj)
    return render(request,"emp-management/list.html",obj)

def edit_employee(request):

    args = {
        'enter':0,

    }
    if(request.method == 'POST'):
        id = request.POST.get('e_id')
        id2 = request.POST.get('eid')
        obj= Employee.objects.raw('SELECT * FROM Shop_employee where e_id = %s',[id])
        args={'obj': obj,'enter':1,'id':id}
        if(id2 is not None):
            print("i in the if")
            if "Edit" in request.POST:
                f_name = request.POST.get('f_name')
                l_name = request.POST.get('l_name')
                wage= request.POST.get('wage')
                contact = request.POST.get('contact')
                address = request.POST.get('address')
                with connection.cursor() as cursor:
                    cursor.execute('UPDATE Shop_employee set f_name = %s, l_name= %s, wage= %s, contact =%s, address= %s where e_id = %s',[f_name,l_name,wage,contact,address,id2])
                obj= Employee.objects.raw('SELECT * FROM Shop_employee where Shop_employee.e_id = %s',[id])
                args={'obj': obj,'enter':1,'id':id}

            elif "Delete" in request.POST:
                c = connection.cursor()
                c.execute('delete from Shop_employee where e_id = %s',[id2])
                obj= Employee.objects.raw('SELECT * FROM Shop_employee where Shop_employee.e_id = %s',[id])
                args={'obj': obj,'enter':1,'id':id}

        
    return render(request,'emp-management/mod.html',args)

def showform(request):

    error = 13
    if request.method=='POST':
        form = AddEmployee(request.POST)
        if form.is_valid():
            form.save()
            error = 0
        else:
            error = 1

    else:
        form = AddEmployee()
        
    context = {'form':form ,'error':error}
    return render(request,"emp-management/addrem.html",context)
@csrf_exempt
def logform(request):
    
    c = connection.cursor()
    args ={
        'error_id':0
    }
    if request.method == 'POST':
        id = request.POST.get('e_id')
        print(id)
        now = datetime.now()
        today = date.today()
        current_date = today.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M:%S")
        test=request.POST.get('In')
        print(test)
        if "In" in request.POST:

            try:
                rec = LogRecord(date=current_date,sign_in=current_time,e_id_id=id,sign_out=None)
                rec.save()
                args  ={
                    'error_id' :13
                }
            except:
                args={
                    'error_id':1
                }
        elif "Out" in request.POST:
            try:
                c.execute('Update Shop_logrecord set sign_out  = %s where e_id_id = %s AND sign_out is NULL',[current_time,id])
                args  ={
                'error_id' :13
                }
            except:
                args={
                    'error_id':1
                }

    print(args)
    return render(request,'log.html',args)



