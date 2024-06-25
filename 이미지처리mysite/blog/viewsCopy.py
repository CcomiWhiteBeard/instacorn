
from django.shortcuts import render, redirect
from django.http  import HttpResponse
from django.db  import connection 
# from django.shortcuts import redirect 

import datetime
import time

# Create your views here.
#url(r'^$', views.first),  http://127.0.0.1:8000/
def first(request):
    print('first method')
    str='<h1> first(request) method </h1> '
    return  HttpResponse(str)


#url(r'^([0-9]{2,4})/', views.two),  http://127.0.0.1:8000/79/
def two(request, num):
    print('two method')
    str='<h1>two(requst,num) num={}</h1>'.format(num)
    return  HttpResponse(str)

#url(r'^([a-zA-Z]{2,7})/', views.three),  http://127.0.0.1:8000/coffee/
def three(request, msg):
    print('three method')
    str='<h1>three(requst,msg) msg={}</h1>'.format(msg)
    return  HttpResponse(str)


#blog어플 views.py문서 생성
def  blogtest(request):
    print('blog어플 blogtest(request): 메소드')
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
    return render(request, 'blog/blogtest.html', context)
   

#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
def  blogwrite(request):
    print('blog어플 blogwrite(request): 메소드 입력화면 이동')
    return render(request, 'blog/blogwrite.html')

#from django.db  import connection  상단에 선언

#저장처리
def  blogsave(request):
    print('blog어플 blogsave(request): 저장처리 insert ~~ ')
    
    if request.method=='GET':
        return render(request, 'blog/blogwrite.html')
    elif request.method=='POST':
        dcode = request.POST.get('code') #request.getParameter("code")
        dname = request.POST.get('name')
        dtitle = request.POST.get('title') 
        print(f'06-12-수요일 넘어온 데이터 코드={dcode}, 이름={dname}, 제목={dtitle}\n')

        # from django.db  import  connection
        cursor = connection.cursor() 
        msg = f"insert into test(code,name,title) values({dcode}, '{dname}', '{dtitle}')"
        cursor.execute(msg)
        connection.commit()
        connection.close()
        print(dcode, '코드 데이터 테이블 저장성공입니다 ')
    #return render(request, 'blog/blogselect.html')
    return redirect('blogselect.do')


#전체출력처리및 데이터갯수
def  blogselect(request):
    print('blog어플 blogselect(request): 전체출력 ')
    dt = datetime.datetime.now()
    print(dt.strftime('현재날짜 %Y년-%m월-%d일 %H시:%M분:%S초\n'))

    cursor = connection.cursor() 
    #원본 msg = "select * from test "
    msg = "select  @rownum:= @rownum+1 as rn , code, name, title, wdate from test , (select @rownum:=0) rowTable  ; "
    cursor.execute(msg)
    rows = cursor.fetchall()

    result = []
    for data in rows:
        row = {'rn':int(data[0]) ,'code':data[1], 'name':data[2],'title':data[3],'wdate':data[4].strftime('%Y년-%m월-%d일') }
        result.append(row)


    msg = "select count(*) as cnt from test "
    cursor.execute(msg)
    total = cursor.fetchall()[0][0]

    mydata = { 
        'total' : total ,
        'result' : result
    }
    return render(request, 'blog/blogselect.html', mydata)


#한건상세
def  blogdetail(request):
    print('blog어플 blogdetail(request) 한건상세출력  ')
    dt = datetime.datetime.now()
    print(dt.strftime('현재날짜 %Y년-%m월-%d일 %H시:%M분:%S초\n'))

    idx = request.GET.get('idx') #dcode = request.POST.get('code')
    print('상세문서코드 idx =' , idx)
    msg = "select * from test where code =  " + idx
    cursor = connection.cursor() 
    cursor.execute(msg)
    # rows = cursor.fetchall()  
    data = cursor.fetchone()
    connection.commit()
    connection.close()
    print('- ' * 60)
    print(' data 결과 ' , data)

    result = {'code':data[0], 'name':data[1],'title':data[2],'wdate':data[3].strftime('%Y년-%m월-%d일 %H시:%M분:%S초') }
    print(' result 결과 ' , result)
    return render(request, 'blog/blogdetail.html', {'result': result})



#한건삭제
def blogdelete(request):
    print('blog어플 blogdelete(request): 삭제처리 delete ~~')
    idx = request.GET.get('idx')  
    cursor = connection.cursor()
    msg = "delete from test where code = " + idx
    cursor.execute(msg)
    connection.commit()
    connection.close()
    print(idx ,'코드 데이터 삭제 성공입니다')
    return redirect('blogselect.do')


#한건 수정
def blogupdate(request):
    print('blog어플 blogupdate(request): 수정전 화면 뿌리기')
    idx = request.GET.get('idx')   #code 
    cursor = connection.cursor()
    msg = "select * from test where code = " + idx
    cursor.execute(msg)
    row = cursor.fetchone() 
    connection.commit()
    connection.close()

    dcode = row[0]
    dname = row[1]
    dtitle = row[2]
    print(dcode, dname, dtitle)
    return render(request, 'blog/blogupdate.html', {'dcode': dcode, 'dname': dname, 'dtitle': dtitle} ) 


#진짜수정처리 
def blogupdatesave(request):
    print('blog어플 blogupdatesave(request): update ~~ 수정처리 ')
    if request.method=='GET':
        pass
    elif request.method=='POST':
        dcode = request.POST.get('code') 
        dname = request.POST.get('name') 
        dtitle = request.POST.get('title') 
        print(f'updatesave 넘어온 데이터 코드={dcode}, 이름={dname}, 제목={dtitle}')

        cursor = connection.cursor()
        msg = f"update test set name = '{dname}', title = '{dtitle}' , wdate = now()  where code = " + dcode
        cursor.execute(msg)
        connection.commit()
        connection.close()
        print(dcode, '코드 데이터 수정성공입니다')
    return redirect('blogselect.do')