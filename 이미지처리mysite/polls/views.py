# Create your views here.
from django.shortcuts import render
from django.http  import HttpResponse


#polls어플 views.py문서 생성
def  pollscheck(request):
    print('polls어플 pollscheck(request): 메소드')
    return render(request, 'polls/pollscheck.html')
   