from django.db import models

class Employee(models.Model):
    e_id = models.IntegerField('E_id')
    f_name = models.CharField('First Name',max_length=20)
    l_name = models.CharField('Last Name',max_length=20)
    wage = models.IntegerField('Wage')
    contact = models.IntegerField('')
    