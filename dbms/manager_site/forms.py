from django import forms
from Shop.models import Employee


class AddEmployee(forms.ModelForm):
    
    class Meta:
        model = Employee
        fields = ("e_id","f_name","l_name","wage","contact","address",)

class EditEmployee(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ("e_id","f_name","l_name","wage","contact","address",)
