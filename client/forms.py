from django import forms
from client.models import CnfOrder

class CnfOrderForm(forms.ModelForm):
    class Meta:
        model = CnfOrder
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'address_line_1', 'address_line_2', 'city', 'state', 'zipcode', 'ship_to_different_address', 'order_notes',]
        
