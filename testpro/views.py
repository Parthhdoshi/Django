from django.shortcuts import render
from django.contrib.auth.models import *
from django.contrib.auth.forms import *
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout 
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect,reverse
from django.conf.urls import url
from .forms import SignUpForm
from django.contrib.auth.models import User, auth, AbstractBaseUser, BaseUserManager
from django.contrib import messages
from testpro.models import Profile, Query, AdDetail
from .forms import *
from .filters import *
from django.forms import inlineformset_factory
from testpro.models import *
from .views import logout
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required
from .decoretors import *
from django.contrib.auth.models import Group

EMAIL_HOST_USER = 'college.parthhdoshi@gmail.com'
# Create your views here.

@unauth_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = form.cleaned_data.get('username')
            
            # group = Group.objects.get(name='customer')
            # user.groups.add(group)
            # Customer.objects.create(user=user,name=user.username)
            messages.success(request,'account has been created for ' + user)
            return redirect('loginpage')
    context = {'form':form}
    return render(request,"registerpage.htm",context)


def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username ,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect("ads")
        else:
            messages.info(request,"Invalid Username OR Password")
            return redirect('login')
    else:
        return render(request, "loginpage.htm")


def home(request):
    return render(request, "home.htm")


def usersetting(request):
    user = request.user.czustomer
    form = CustomerUpdateForm(instance = user)

    if request.method == "POST":
        form = CustomerUpdateForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
    context = {
        'form':form
    }
    return render(request, "usersetting.htm",context)


@login_required(login_url='loginpage') 
def userpage(request):
    
    customer = Customer.objects.all()
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()

    orders_delivered = orders.filter(status='Delivered').count()
    orders_pending = orders.filter(status='Pending').count()
    print(orders_pending)
    context = {

        'customer':customer,
        'orders':orders,
        'total_orders' : total_orders,
        'orders_delivered' : orders_delivered,
        'orders_pending' : orders_pending
    }
    return render(request,'userpage.htm',context)

@login_required(login_url='loginpage') 
@allowed_user(allowed_roles=['admin'])
def ads(request):
    
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customer = customers.count()
    total_orders = orders.count()

    orders_delivered = orders.filter(status='Delivered').count()
    orders_pending = orders.filter(status='Pending').count()

    context = {'orders':orders, 'customers':customers,'total_customer':total_customer,
    'total_orders':total_orders,'orders_delivered':orders_delivered,
    'orders_pending':orders_pending
    }
    return render(request,'ads.htm',context)

@login_required(login_url='login') 
def profile(request,pk_test):
    adver = Advertise.objects.all()
    # users = User.objects.get(id=pk_test) 
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    place = Places.objects.all()
    print(adver)
    my_filters = OrderFilter(request.GET,queryset=orders)
    orders = my_filters.qs 
    context = {
    'adver':adver,
    'place':place,
    'customer':customer,
    'orders':orders,
    'my_filters':my_filters,
    # 'users':users
    }
    return render(request,'profile.htm',context)


def login(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username ,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect("shopkeeper")
        else:
            messages.info(request,"NOT LOGGED IN")
            return redirect('login')
    else:
        return render(request, "login.htm")

def logoutpage(request):
    logout(request)
    return redirect('loginpage')

def logout(request):
    auth.logout(request)
    return redirect('home')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # user.refresh_from_db()  # load the profile instance created by the signal
            # user.profile.profile = form.cleaned_data.get('profile')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password )
            if user is not None:
                auth.login(request, user)
                return redirect('home')
            else:
                return redirect('signup')
    else:
        form = SignUpForm()
    return render(request, 'signup.htm', {'form': form})


def emailView(request):
    if request.method == 'GET':
        form = ContactForm(request.GET)
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            b = request.POST['subject']
            a = request.POST['from_email']
            c= " from email :" + a + ", subject: " + b
            subject = c
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            form.save()
            try:
                send_mail(subject, message, EMAIL_HOST_USER, [EMAIL_HOST_USER])
                form.save()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponse("success <h1><a href='/'>home</a></h1> ") 
    return render(request, "email.htm", {'form': form})


def successView(request):
    return HttpResponse('Your Query has been submited {home}')

def about(request):
    return render(request, 'about.htm')

# def advertiser(request):
    # return render(request, 'advertiser.htm')


@login_required(login_url='login')
@allowed_user(allowed_roles=['shopkeeper'])
def shopkeeper(request,pk):
    user = User.objects.get(id=pk)
    adverform = AdvertiserForm()
    post = AdDetail.objects.all()

    if request.method == "POST":    
        forms = AdvertiserForm(request.POST)
        if forms.is_valid():
            forms.save()
    
    context = {
        'post':post,
        'adverform':adverform
    }
    return render(request, 'shopkeeper.htm', context)

@login_required(login_url='login') #redirect when user is not logged in
def advertiser(request,pk):
    user = User.objects.get(id=pk)
    adform = ADSForm(initial={'users':user})
    post = AdDetail.objects.all()

    if request.method == "POST":

        forms = ADSForm(request.POST, request.FILES)
        if forms.is_valid():
            forms.save()
    
    context = {
        'post':post,
        'adform':adform
    }
    return render(request, 'advertiser.htm', context)

def createorder(request,pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','place','adver'),extra=1)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # print('Printing POST', request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('ads')
    context = {'form':formset}
    return render(request,'order_form.htm',context)

def updateorder(request,pk):
    orders = Order.objects.get(id=pk)
    form = OrderForm(instance=orders)
    if request.method == 'POST':
        # print('Printing POST', request.POST)
        form = OrderForm(request.POST, instance=orders)
        if form.is_valid():
            form.save()
            return redirect('ads')
    context = {'form':form}
    return render(request,'order_form.htm',context)

def deleteorder(request,pk):
    orders = Order.objects.get(id=pk)
    if request.method == "POST":
        orders.delete()
        return redirect('ads')

    context = {'item':orders}
    return render(request,'delete_order.htm',context)
