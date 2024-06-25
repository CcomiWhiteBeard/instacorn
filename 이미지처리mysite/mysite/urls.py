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
from django.contrib import admin
from django.urls import path
from .  import views
from .  import settings 
from django.urls import include 


# views.py문서 처리함수작성 ~~~ render(요청, html문서, 넘기는값 )
# urls.py문서에 매핑  views문서이름.함수 

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index, name='index') ,
    #비권장 path('blog/', include('blog.urls')) ,
    path('', include('blog.urls')) ,
    path('', include('sns.urls')) ,
    path('', include('polls.urls')) , 
    path('', include('kakao.urls')) , 
] 
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
