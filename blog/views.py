
from django.shortcuts import render, redirect
from django.http  import HttpResponse
from django.db  import connection 
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage  
# FileSystemStorage클래스  43라인에 MEDIA_ROOT
from django.views.decorators.csrf import csrf_exempt

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


#저장처리-원본 img_file없는상태에서 
def  blogsave3(request):
    print('blog어플 blogsave(request): 저장처리 insert ~~ ')
    
    if request.method=='GET':
        return render(request, 'blog/blogwrite.html')
    elif request.method=='POST':
        dcode = request.POST.get('code') #request.getParameter("code")
        dname = request.POST.get('name')
        dtitle = request.POST.get('title') 
   
        print(f'넘어온 데이터  코드={dcode}, 이름={dname}, 제목={dtitle}\n')
    
        # from django.db  import  connection
        cursor = connection.cursor() 
        msg = f"insert into test(code,name,title) values({dcode}, '{dname}', '{dtitle}')"
        cursor.execute(msg)
        connection.commit()
        connection.close()
        print(dcode, '코드 데이터 테이블 저장성공입니다 ')
    #return render(request, 'blog/blogselect.html')
    return redirect('blogselect.do')

#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------
#저장처리 - 이미지저장처리 
def  blogsave(request):
    print('blog어플 blogsave(request): 저장처리 insert ~~ ')
    
    if request.method=='GET':
        return render(request, 'blog/blogwrite.html')
    elif request.method=='POST':
        dcode = request.POST.get('code') 
        dname = request.POST.get('name')
        dtitle = request.POST.get('title') 
        dimg_file = request.FILES.get('img_file')
        
        print(f'06-14-금요일 넘어온 데이터  파일={dimg_file}, 코드={dcode}, 이름={dname}, 제목={dtitle}\n')
    
        fs = FileSystemStorage(location='media/images')
        fs.save(request.FILES.get('img_file').name, request.FILES.get('img_file'))

        # from django.db  import  connection
        cursor = connection.cursor() 
        msg = f"insert into test(code,name,title,img_file) values({dcode}, '{dname}', '{dtitle}', '{dimg_file}')"
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

    #검색키워드
    skey = request.GET.get('keyfield')
    sval = request.GET.get('keyword')
    if(skey=="" or skey==None or sval=="" or sval==None):
        skey="name" # select code, name, title, wdate from test
        sval=''     # select code, name, title, wdate from test where name like '%%' ;

    #페이징쪼개기 
    pageNum = request.GET.get('page')
    if pageNum==None:
        pageNum=1

    pageNum = int(pageNum)  # [이전] [11][12] ~~[16서경]~ [19][20][다음]
    startRow = (pageNum*10)-9  #151
    endRow = pageNum*10        #160

    temp = (pageNum-1)%10    #5
    startpage = pageNum-temp #16-5 
    endpage = startpage+9    #11+9=20
    returnpage = "&keyfield="+skey+"&keyword="+sval
    pageCount = 13

    cursor = connection.cursor() 

    #원본   msg = "select * from test "
    #행번호 msg = """select  @rownum:= @rownum+1 as rn ,  code, name, title, wdate from test , (select @rownum:=0) rowTable  """
    
    msg3 = f""" 
            SELECT * FROM (
                SELECT @ROWNUM:=@ROWNUM+1 as rn, A.*
                (SELECT COUNT(*) from testreply r  WHERE r.rcode=A.code) as rcnt from
                  (SELECT * from test where {skey} like '%{sval}%') A, (SELECT @ROWNUM:=0) rowTable
            ) my WHERE rn BETWEEN {startRow} AND {endRow} """
    
    msg2 = f""" 
            SELECT * FROM (
                SELECT @ROWNUM:=@ROWNUM+1 as rn, A.*, 
                (SELECT COUNT(*) from testreply r  WHERE r.rcode=A.code) as rcnt from
                  (SELECT * from test where {skey} like '%{sval}%') A, (SELECT @ROWNUM:=0) rowTable
            ) my WHERE rn BETWEEN {startRow} AND {endRow} """

    print(msg2)
    print()
    cursor.execute(msg2)
    rows = cursor.fetchall()
    connection.commit()

    result = []
    for data in rows:
        row = {'rn':int(data[0]) ,'code':data[1], 'name':data[2],
               'title':data[3], 'wdate':data[4].strftime('%Y년-%m월-%d일'), 'img_file':data[5], 'rcnt':data[6] }       
        result.append(row)


    msg7 = "select count(*) as cnt from test "
    cursor.execute(msg7)
    total = cursor.fetchall()[0][0]

    msg8 = f"select count(*) as cnt from test  where {skey}  like '%{sval}%'  "
    cursor.execute(msg8)
    stotal = cursor.fetchall()[0][0]
    
    if (stotal%10==0):
        pageCount = stotal/10
    else:
        pageCount = (stotal/10)+1


    mydata = { 
        'result' : result ,
        'startPage' : startpage,
        'endPage' : endpage,
        'returnpage' : returnpage,
        'pageNum' : pageNum,
        'total' : total,
        'stotal' : stotal,
        'pageCount' : pageCount,
    }
    return render(request, 'blog/blogselect.html', mydata)


#한건상세
def  blogdetail(request):
    print('blog어플 blogdetail(request) 한건상세출력  ')
    dt = datetime.datetime.now()
    print(dt.strftime('현재날짜 %Y년-%m월-%d일 %H시:%M분:%S초\n'))
    mycount = 0

    idx = request.GET.get('idx') #dcode = request.POST.get('code')
    print('상세문서코드 idx =' , idx)
    msg = "select * from test where code =  " + idx
    cursor = connection.cursor() 
    cursor.execute(msg)
    datas = cursor.fetchall()  
    #data = cursor.fetchone()
    result = []
    for data in datas:
        dto = {'code':data[0], 'name':data[1],'title':data[2],'wdate':data[3].strftime('%Y년-%m월-%d일 %H시:%M분:%S초'),'img_file':data[4] }
        mycount = mycount + 1
        result.append(dto)


    #msg="""select  @rownum:= @rownum+1 as rn ,  code, name, title, wdate from test , (select @rownum:=0) B  """
    msg_reply = f"""select @rownum:=@rownum+1 as rrn, 
                    r.* from testreply r , (select @rownum:=0) B  where rcode = {idx} """
    cursor.execute(msg_reply)
    replydatas = cursor.fetchall()     
    replyresult=[]
    for row in replydatas:
        data={'rrn':int(row[0]), 'rnum':row[1], 'rwriter':row[2], 'rmemo':row[3], 'rcode':row[4]}
        replyresult.append(data)

    myresult = { 'result':result[0], 'replyresult':replyresult , 'mycount':mycount}
    return render(request, 'blog/blogdetail.html', myresult)



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



#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------
#댓글저장,수정,삭제처리 
#from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def blog_replyinsertsave(request):
    print('댓글저장 blog_replyinsertsave(request):')
    if request.method == 'GET':
        return  redirect('blogselect.do')
    elif request.method == 'POST':
        rwriter = request.POST.get('rwriter')
        rmemo = request.POST.get('rmemo')
        rcode = request.POST.get('rcode')

        cursor = connection.cursor()
        msg = f"insert into testreply(rwriter,rmemo,rcode) values('{rwriter}', '{rmemo}', {rcode})"
        cursor.execute(msg)
        connection.commit()
        connection.close()

    return redirect('blogdetail.do?idx=' + rcode)


def blog_replydeletesave(request):
    print('댓글삭제 blog_replydeletesave(request):')  
    idx = request.GET.get('idx')
    ridx = request.GET.get('ridx')
    print('댓글삭제 rcode=' , idx , ' rnum=' , ridx)
    
    msg = f"delete from testreply where rnum ={ridx} "
    cursor = connection.cursor()
    cursor.execute(msg)
    connection.commit()
    connection.close()
    #비권장 return redirect('blogdetail.do?idx=' + idx)
    return redirect(f'blogdetail.do?idx={idx}')



def blog_replyupdatesave(request):
    print('댓글수정 blog_replyupdatesave(request):')
    if request.method == 'GET':
        return  redirect('blogselect.do')
    elif request.method == 'POST':
        rnum = request.POST.get('rnum') 
        rwriter = request.POST.get('rwriter')
        rmemo = request.POST.get('rmemo')
        rcode = request.POST.get('rcode')

        cursor = connection.cursor()
        msg = f"update testreply set rwriter = '{rwriter}', rmemo = '{rmemo}', rcode = '{rcode}' where rnum = {rnum}"
        cursor.execute(msg)
        connection.commit()
        connection.close()
        print(rnum, ' 댓글 수정 완료')

    return redirect('blogdetail.do?idx=' + rcode)


