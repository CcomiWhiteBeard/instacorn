from django.shortcuts import render
from django.http  import HttpResponse

# views.py문서 처리함수작성 ~~~ render(요청, html문서, 넘기는값 )
# urls.py문서에 매핑  views문서이름.함수 

def  index(request):
    print('처음작성 10시 45분  index(request): ')
    return render(request, 'index.html')
    #templates폴더아래에 있는 index.html