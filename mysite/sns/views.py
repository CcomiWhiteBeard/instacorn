from django.shortcuts import render

# Create your views here.

#sns어플  views.py문서
def  snsnaver(request):
    print('sns어플 snsnaver(request): 메소드')
    return render(request, 'sns/snsnaver.html')
   