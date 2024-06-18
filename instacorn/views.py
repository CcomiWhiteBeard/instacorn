from django.shortcuts import render, redirect
from django.http  import HttpResponse
from django.db  import connection 
from django.core.files.storage import FileSystemStorage  
from django.views.decorators.csrf import csrf_exempt

#테스트용. 지워도 됨
def  instest(request):
    msg = "select * from test " 
    cursor = connection.cursor() 
    cursor.execute(msg)
    datas = cursor.fetchall()  
    
    result = []
    for data in datas:
        dto = {'code':data[0], 'name':data[1],'title':data[2],'wdate':data[3].strftime('%Y년-%m월-%d일 %H시:%M분:%S초'),'imgname':data[4] }
        result.append(dto)
    
    myresult = { 'result':result, }
    return render(request, 'instacorn/main.html', myresult)