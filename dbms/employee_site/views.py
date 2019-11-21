from django.shortcuts import render
from Shop.models import Sale,Products,ExpiryDetails,SalesRecord
from django.db import connection,transaction
from datetime import datetime,date
# Create your views here.
def employee_sales_view(request):
	x= Sale.objects.raw(" SELECT * FROM Shop_sale")
	gtotal=0
	for l in x:
		gtotal=gtotal+l.total_price
	obj={
		'table':x,
		'gtotal':gtotal
	}
	if request.method == "POST":

		pid=request.POST.get('p_id')
		if pid is not None:
			qty=request.POST.get('qty')
			pid=int(pid)
			qty=int(qty)
			if(qty==0):
				return render(request,"employee_sales.html",obj)
			x=Products.objects.raw("SELECT * FROM Shop_products WHERE Shop_products.p_id = %s",[pid])
			if (len(x)==0):
				obj['error1']=1
				return render(request,"employee_sales.html",obj)
			print(x[0].quantity)
			if(x[0].quantity<qty):
				obj['error2']=1
				return render(request,"employee_sales.html",obj)
			name=x[0].typE
			company=x[0].company
			category=x[0].category
			price=x[0].price
			totalprice=price*qty
			x=ExpiryDetails.objects.raw("SELECT * FROM Shop_expirydetails WHERE Shop_expirydetails.p_id_id = %s",[pid])
			tempqty=qty
			c=connection.cursor()
			for y in x:
				if tempqty==0:
					break
				if y.quantity<=tempqty:
					tempqty=tempqty-y.quantity
					
					c.execute('DELETE FROM Shop_expirydetails WHERE Shop_expirydetails.p_id_id = %s AND Shop_expirydetails.date = %s',[y.p_id.p_id,y.date])
				else:
					tempqty=y.quantity-tempqty
		
					c.execute('UPDATE Shop_expirydetails SET quantity = %s WHERE p_id_id = %s AND date = %s',[tempqty,y.p_id.p_id,y.date])
					transaction.commit()
					break
			c.execute('UPDATE Shop_products SET quantity = quantity - %s WHERE p_id = %s',[qty,pid])
			transaction.commit()
			c.execute('INSERT INTO Shop_sale VALUES (%s,%s,%s,%s,%s,%s,%s) ',[pid,name,company,category,qty,price,totalprice])
			x=SalesRecord.objects.raw("SELECT * FROM Shop_salesrecord")
			rid=0
			for y in x:
				rid=rid+1
			rid=rid+1
			datetemp=date.today()
			date5=str(datetemp.year)+"-"+str(datetemp.month)+"-"+str(datetemp.day)
			totalprice=int(totalprice)
			c.execute('INSERT INTO Shop_salesrecord VALUES (%s,%s,%s,%s,%s) ',[rid,date5,totalprice,qty,pid])
			x= Sale.objects.raw(" SELECT * FROM Shop_sale")
			gtotal=0
			for l in x:
				gtotal=gtotal+l.total_price
			obj={
				'table':x,
				'gtotal':gtotal
				}
			obj['success1']=1
			return render(request,"employee_sales.html",obj)		
		else:
			total=0
			x=Sale.objects.raw("SELECT * FROM Shop_sale")
			for y in x:
				total=total+y.total_price
			c=connection.cursor()
			c.execute('DELETE FROM Shop_sale')
			x=Sale.objects.raw("SELECT * FROM Shop_sale")
			obj={
				'table':x,
				'gtotal':0
				}
			obj['total1']=total
			return render(request,"employee_sales.html",obj)		
	return render(request,"employee_sales.html",obj)

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
def employee_viewall_view(request):
	print("text")
	x=Products.objects.raw(" SELECT Shop_products.p_id, Shop_products.price, Shop_products.typE, Shop_products.company, Shop_products.category, Shop_products.s_id_id, Shop_expirydetails.quantity AS expqty ,Shop_products.quantity, Shop_expirydetails.date FROM Shop_products LEFT JOIN Shop_ExpiryDetails ON Shop_Products.p_id = Shop_ExpiryDetails.p_id_id ORDER BY Shop_Products.p_id , Shop_Products.category , Shop_ExpiryDetails.date")
	obj={
		'table':x
	}
	if request.method == "POST":
		x=ExpiryDetails.objects.raw("SELECT * FROM Shop_expirydetails")
		cdate=datetime.date(datetime.now())
		print(cdate)
		for i in x :
			print(type(i.date), i.date)
			edate=parsedate1(i.date)
			pid= i.p_id.p_id
			qty=i.quantity
			if(edate.date() < cdate):
				c=connection.cursor()
				c.execute('DELETE FROM Shop_expirydetails WHERE date=%s AND Shop_expirydetails.p_id_id= %s',[i.date,pid])
				c.execute('UPDATE Shop_products SET quantity=quantity-%s WHERE p_id=%s',[qty,pid])
		obj['success1']=1
		return render(request,"employee_viewall.html",obj)
	return render(request,"employee_viewall.html",obj)