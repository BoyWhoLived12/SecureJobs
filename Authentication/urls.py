# from django.contrib import admin
from django.urls import path, include
from Authentication.views import *


urlpatterns = [
    path('login', login_user, name='login'),
    path('register', register_user, name='register'),
    path('c_account', account_company, name='c_account'),
    path('p_account', account_personal, name='p_account'),
    path('job_post', job_post, name='job_post'),
]
