# views.py문서 처리함수작성을 함 ~~~ render(요청, html문서, 넘기는 값)
# urls.py문서에 맵핑을 함

from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    print('6월 17일 인스타클론코딩을 하기 위해 작성')
    return render(request, 'index.html')