from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from .models import *
from django.forms import ModelForm
from django.core.validators import RegexValidator

alphanumeric = RegexValidator(r'^[a-zA-Z]*$', 'Only alpha characters are allowed.')

PROFILE_CHOICES=( 
    ("Shopkeeper", "Shopkeeper"), 
) 

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30,  help_text='Char Value.',validators=[alphanumeric])
    last_name = forms.CharField(max_length=30, help_text='Char Value.', validators=[alphanumeric] )
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    role = forms.CharField(
        max_length=20,
        widget=forms.Select(choices=PROFILE_CHOICES),
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'role','email', 'password1', 'password2')
        
class ContactForm(forms.ModelForm):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Query
        fields = ('from_email','subject','message')

class AdvertiserForm(ModelForm):
    class Meta:
        model = AdDetail
        fields = '__all__'
        exclude = ['user',]

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class ADSForm(ModelForm):
    class Meta:
        model = Advertise
        fields = '__all__'
        # exclude = ['users',]
        
class CustomerUpdateForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['users']

class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30,  help_text='Char Value.',validators=[alphanumeric])
    last_name = forms.CharField(max_length=30, help_text='Char Value.', validators=[alphanumeric] )
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2',]