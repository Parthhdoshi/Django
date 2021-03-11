from django.contrib import admin
from .models import *

admin.site.site_header = 'DIGI FLYER'

# Register your models here.

admin.site.register(Profile)
admin.site.register(Query)
admin.site.register(AdDetail)
admin.site.register(UsersRole)
admin.site.register(Tag)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Places)
admin.site.register(Advertise)


