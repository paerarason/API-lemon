from django import forms  
class MenusForm(forms.Form): 
    title = forms.CharField(max_length=255)
    price = forms.DecimalField(max_digits=6, decimal_places=2)
    inventory =forms.SmallIntegerField()
    