from django.shortcuts import render
import datetime
from .models import Person
from django.http import HttpResponse
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def  kakaotest(request):
    print('kakao어플 kakaotest(request): 메소드')
    #문자 message ='여름수박추천 겨울체리추천'
    #문자 return render(request, 'blog/blogtest.html', {'kim':message})

    #딕트 board = { 'code': 2400, 'name':'hong', 'title': 'summer' }
    #딕트 return render(request, 'blog/blogtest.html', board )

    context = {
        'boardTable': [
            { 'code': 1200, 'name':'aaa', 'title': 'summer'},
            { 'code': 2400, 'name':'bbb', 'title': 'winter'},
            { 'code': 3500, 'name':'ccc', 'title': 'spring'}
        ] 
    }
    return render(request, 'kakao/kakaotest.html', context)




#-------------------------------------------------------------------------------------------------------------
def  kakaowrite(request):
    print('kakao어플 kakaowrite(request): 메소드 입력화면 이동')
    return render(request, 'kakao/kakaowrite.html')



def  kakaosave(request):
    print('kakao어플 kakaosave(request): 저장처리 insert ~~ ')
    if request.method=='GET':
        return render(request, 'blog/blogwrite.html')
    else:
        pass

    return render(request, 'kakao/kakaoselect.html')


#전체출력
def  kakaoselect(request):
    print('kakao어플 kakaoselect(request): 전체출력 ')
    dt = datetime.datetime.now()
    print(dt.strftime('현재날짜 %Y년-%m월-%d일 %H시:%M분:%S초\n'))

    myperson = Person.objects.all()
    print(myperson)
    count = myperson.count()
    data = {'myperson':myperson, 'count':count} 
    return render(request, 'kakao/kakaoselect.html')