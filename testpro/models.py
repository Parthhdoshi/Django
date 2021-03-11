from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm
from django.core.validators import RegexValidator


# Create your models here. 

class Places(models.Model):
    name = models.CharField(max_length=50,null=True)

    def  __str__(self):
        return self.name    

class Tag(models.Model):
    name = models.CharField(max_length=200,null=True) 

    def  __str__(self):
        return self.name

class Customer(models.Model):
    users = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=200,null=True)
    email = models.EmailField(max_length=200,null=True)
    profile_pic = models.ImageField(default="default.jpg",null=True, blank=True)  
    date_created = models.DateTimeField(auto_now=True,null=True)

    def  __str__(self):
        return self.name

class Advertise(models.Model):
    users = models.ForeignKey(Customer,null=True, on_delete=models.CASCADE)
    adname = models.CharField(max_length=500)
    ads = models.FileField(upload_to='ads', max_length=100)

    def  __str__(self):
        return self.adname

class Product(models.Model):
    CATEGORY = (
			('Online', 'Online'),
			('Offline', 'Offline'),
			) 
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200,null=True,choices=CATEGORY)
    discription = models.CharField(max_length=200,null=True,blank=True) 
    date_created = models.DateTimeField(auto_now=True,null=True)
    place = models.ManyToManyField(Places)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (  ('Pending', 'Pending'),
	 		('Out for delivery', 'Out for delivery'),
	 		('Delivered', 'Delivered'),)
    customer = models.ForeignKey(Customer,null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product,null=True, on_delete=models.SET_NULL)
    place = models.ForeignKey(Places,null=True,on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS, default='Pending')
    note = models.CharField(max_length=500, null=True, blank=True)
    adver = models.ForeignKey(Advertise,null=True, on_delete=models.CASCADE)


    def __str__(self):
        return self.product.name



class Query(models.Model):
    from_email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return self.from_email

class AdDetail(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    comp_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    place = models.CharField(max_length=50)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
      


PROFILE_CHOICES=( 
    ("Advertiser", "Advertiser"), 
    ("Shopkeeper", "Shopkeeper"), 
) 

class UsersRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=PROFILE_CHOICES)

    def __str__(self):
        return self.role

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UsersRole.objects.create(user=instance)

    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_img')

    def __str__(self):
        return f'{self.user.username} Profile'
