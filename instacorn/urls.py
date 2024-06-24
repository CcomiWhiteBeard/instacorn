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
    #테스트용 지워도 됨
    path('instest.do', views.instest) ,
    
    #메인페이지
    path('instahome.do', views.instahome),
    
    #검색페이지
    path('instaselect.do', views.instaselect)

    #상세페이지


    #마이페이지


    #댓글
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
