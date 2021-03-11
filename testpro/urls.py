from django.urls import path, include
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth import logout
from .views import logout
from django.conf import settings
from django.conf.urls.static import static 


urlpatterns = [
    path('',views.home, name='home'),
    path('home',views.home, name='home'),
    path('signup',views.signup, name='signup'),
    path('login', views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('ads',views.ads, name='ads'),
    path('email', views.emailView, name='email'),

# in this url patten login/ and  login bare both different meaning 
    path('register' ,views.registerPage,name='registerpage'),
    path('loginpage',views.loginpage,name='loginpage'),
    path('logout',views.logoutpage,name='logoutpage'),

    path('user',views.userpage,name='userpage'),
    path('user/usersetting',views.usersetting,name='usersetting'),

    path('profile/<str:pk_test>', views.profile, name='profile'),
    path('create_order/<str:pk>', views.createorder, name='create_order'),
    path('Update/<str:pk>', views.updateorder, name='update_order'),
    path('delete/<str:pk>', views.deleteorder, name='delete_order'),

    path('about',views.about, name='about'),
    path('advertiser/<str:pk>',views.advertiser, name='advertiser'),
    path('shopkeeper/<str:pk>',views.shopkeeper, name='shopkeeper'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.htm'), name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.htm'), name='password_change'),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.htm'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.htm'), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.htm'),name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )
     


