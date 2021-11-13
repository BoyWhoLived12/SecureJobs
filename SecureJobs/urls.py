"""SecureJobs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from Authentication.views import home, job_list, job_detail, company_detail, company_list
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('auth/', include('Authentication.urls')),
                  path('', home, name='home'),
                  path('job_list', job_list, name='job_list'),
                  path('company_list', company_list, name='company_list'),
                  path('job_detail/<str:slug>', job_detail, name='job_detail'),
                  path('company_detail/<str:slug>', company_detail, name='company_detail'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
