"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    #메인페이지

    
    #검색페이지


    #상세페이지
    path('insdetail.do', views.insdetail) ,
    path('insdelete.do', views.insdelete) , 
    path('insupdate.do', views.insupdate) ,
    path('insupdatesave.do', views.insupdatesave) ,
    
    #마이페이지


    #댓글
    path('insreplyinsert.do', views.insreplyinsert) ,
    path('insreplydelete.do', views.insreplydelete) ,
    path('insreplyupdate.do', views.insreplyupdate) ,

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
