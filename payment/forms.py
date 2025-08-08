from django import forms
from .models import Address,Payment
from django.core.exceptions import ValidationError
# Create your forms here.

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'phone', 'email', 'country', 'city', 'postal_code', 'apartment', 'address', 'account_create', 'terms_accepted', 'method']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'apartment': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'account_create': forms.CheckboxInput(attrs={'class': 'form-check-input', 'class': 'ml-2'}),
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input', 'class': 'ml-2'}),
            'method': forms.RadioSelect(),
        }
    def clean_terms_accepted(self):
        value = self.cleaned_data.get('terms_accepted')
        if not value:
            raise ValidationError("Please accept the terms and conditions.")
        return value