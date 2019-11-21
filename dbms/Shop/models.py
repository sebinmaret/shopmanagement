from django.db import models

# Create your models here.
class Employee(models.Model):
    e_id = models.IntegerField('Employee id',primary_key=True)
    f_name = models.CharField('First Name',max_length=20)
    l_name = models.CharField('Last Name',max_length=20)
    wage = models.IntegerField('Wage')
    contact = models.IntegerField('Contact')
    address = models.CharField('Address',max_length=50)


class LogRecord(models.Model):
    
    sign_out = models.CharField('Sign Out', max_length=5,null=True)
    date = models.CharField('Date',max_length=10)
    sign_in = models.CharField('Sign in', max_length=5)
    e_id = models.ForeignKey('Employee',on_delete = models.CASCADE)


class Supplier(models.Model):
    s_id = models.IntegerField('Supplier ID',primary_key=True)
    address = models.CharField('Address',max_length=50)
    contact_no = models.IntegerField('Contact number')
    s_name = models.CharField('Supplier Name',max_length=20)

class SupplierCat(models.Model):
    category = models.CharField('Category',max_length=20)
    s_id = models.ForeignKey('Supplier',on_delete = models.CASCADE)
    
    class Meta:
        unique_together= ['category','s_id']

class Products(models.Model):
    p_id = models.IntegerField('Product ID',primary_key=True)
    quantity = models.IntegerField('Quantity',)
    price  = models.FloatField('Price',)
    typE = models.CharField('Type',max_length=20)
    company = models.CharField('Company',max_length=30)
    category = models.CharField('Category',max_length=30)
    s_id = models.ForeignKey('Supplier',on_delete = models.CASCADE)

class ExpiryDetails(models.Model):
    
    date = models.CharField('Date',max_length=10,null=True)
    quantity = models.IntegerField('Quantity')
    p_id = models.ForeignKey('Products',on_delete = models.CASCADE)
    class Meta:
        unique_together=['date','p_id']

class SalesRecord(models.Model):
    r_id = models.IntegerField('Record ID',primary_key=True)
    date = models.CharField('Date',max_length=10)
    total_price = models.IntegerField('Total Price')
    quantity= models.IntegerField('Quantity')
    p_id = models.ForeignKey('Products',on_delete = models.CASCADE,db_constraint=False)

    
class Sale(models.Model):
    p_id = models.IntegerField('Product ID',primary_key=True)
    p_type=models.CharField('Type',max_length=20)
    company=models.CharField('Company',max_length=30)
    category=models.CharField('Category',max_length=30)
    quantity=models.IntegerField('Quantity')
    price=models.FloatField('Price')
    total_price=models.FloatField('Total Price')
