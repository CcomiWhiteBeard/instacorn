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


#blog어플 urls.py문서
urlpatterns = [
    #path(r'^$', views.first),  #http://127.0.0.1:8000/
    #path(r'^([0-9]{2,4})/', views.two),  #http://127.0.0.1:8000/34/
    #path(r'^([a-zA-Z]{2,7})/', views.three),  #http://127.0.0.1:8000/tree/
    path('blogtest.do', views.blogtest) , 
    path('blogwrite.do', views.blogwrite),
    path('blogsave.do', views.blogsave),  #<form action="blogsave.do">
    path('blogselect.do', views.blogselect), 
    path('blogdetail.do', views.blogdetail), 
    
    path('blogdelete.do', views.blogdelete),
    path('blogupdate.do', views.blogupdate),
    path('blogupdatesave.do', views.blogupdatesave),

    #댓글
    path('blog_replyinsertsave.do', views.blog_replyinsertsave),  
    path('blog_replydeletesave.do', views.blog_replydeletesave),
    path('blog_replyupdatesave.do', views.blog_replyupdatesave),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
