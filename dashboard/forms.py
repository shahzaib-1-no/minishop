from django import forms
from .models import (navbar, banner, services, Category, Product)
from django.core.exceptions import ValidationError


class navbarForm(forms.ModelForm):
    class Meta:
        model = navbar
        fields = ['name', 'number', 'email', 'description'] 
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
class bannerForm(forms.ModelForm):
    class Meta:
        model = banner
        fields = ['image', 'name', 'title', 'description'] 
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        
class servicesForm(forms.ModelForm):
    class Meta:
        model = services
        fields = ['icon', 'name', 'description'] 
        widgets = {
            'icon': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        parent = cleaned_data.get('parent')

        if not name:
            return cleaned_data  # nothing to validate

        # ✅ Check: Same name under same parent (original check)
        same_parent = Category.objects.filter(
            name__iexact=name,
            parent=parent
        ).exclude(id=self.instance.id)

        if same_parent.exists():
            if parent:
                self.add_error('name', f"A sub-category named '{name}' already exists under '{parent.name}'.")
            else:
                self.add_error('name', f"A main category named '{name}' already exists.")

        # ✅ Check: If this is a sub-category, name must not match any main category
        if parent:
            top_level = Category.objects.filter(name__iexact=name, parent__isnull=True).exclude(id=self.instance.id)
            if top_level.exists():
                self.add_error('name', f"Cannot use '{name}' as a sub-category because a main category with this name already exists.")

        # ✅ Check: If this is a main category, name must not match any sub-category
        if not parent:
            sub_level = Category.objects.filter(name__iexact=name, parent__isnull=False).exclude(id=self.instance.id)
            if sub_level.exists():
                self.add_error('name', f"Cannot use '{name}' as a main category because it already exists as a sub-category.")

        return cleaned_data

class CategoryModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        prefix = ""
        current = obj
        while current.parent:
            prefix = "— " + prefix
            current = current.parent
        return f"{prefix}{obj.name}"
    
class productForm(forms.ModelForm):
    category = CategoryModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Category"
    )

    class Meta:
        model = Product
        fields = ['image', 'name', 'price', 'quantity', 'category', 'description']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            # 👇 category YAHAN SE REMOVE kar do
            # 'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(productForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()

    def clean_category(self):
        category = self.cleaned_data['category']
        if category.subcategories.exists():
            raise forms.ValidationError("You cannot assign a product to a parent category. Please select a sub-category.")
        return category
    