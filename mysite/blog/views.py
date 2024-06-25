from django.shortcuts import render, redirect
from django.http  import HttpResponse
from django.db import connection
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage


#blog어플 views.py문서

def  blogtest(request):
    print('blog어플이름명시test(request): 메소드')
    context = {
        'boardTable' : [
            {'code':1200, 'name':'aaa', 'title':'summer'},
            {'code':2400, 'name':'bbb', 'title':'winter'},
            {'code':3600, 'name':'ccc', 'title':'spring'}
        ]
    }
    return render(request, 'blog/blogtest.html', context )

def blogwrite(request):
    return render(request, 'blog/blogwrite.html')

def blogsave(request):
    if request.method == 'GET':
        return render(request, 'blog/blogwrite.html')
    elif request.method == 'POST':
        dcode = request.POST.get('code')
        dname = request.POST.get('name')
        dtitle = request.POST.get('title')
        #print(f'code: {dcode}, name: {dname}, title: {dtitle}\n')

        cursor = connection.cursor()
        msg = f"insert into test(code, name, title) values({dcode}, '{dname}', '{dtitle}')"
        cursor.execute(msg)
        connection.commit()
        connection.close()
        print(dcode, '코드 데이터 저장 성공')

    #return render(request, 'blog/blogtest.html')
    return redirect("blogselect.do")
   
def blogselect(request):

    skey = request.GET.get('keyfield')
    sval = request.GET.get('keyword')
    if(skey=="" or skey==None or sval==None):
        skey="name"
        sval=""
    
    pageNum = request.GET.get('page')
    if pageNum == None:
        pageNum=1
    pageNum = int(pageNum)
    start = (pageNum*10)-9
    end = pageNum*10

    temp = (pageNum-1)%10
    startPage = pageNum-temp
    endPage = startPage+9
    returnPage = "&keyfield="+skey+"&keyword="+sval
    pageCount = 13

    
    cursor = connection.cursor()
    cursor.execute("SET @rownum := 0;")
    msg2 = f"""
            select * from (
              select @rownum:=@rownum+1 AS rn, 
              A.*, 
              (select count(*) from testreply r where r.rcode=A.code) as rcnt 
                    from (select * from test where {skey} like '%{sval}%') A, (SELECT @rownum:=0) rowTable
            ) my where rn between {start} and {end}

        """
    msg = """
    SELECT 
        ROW_NUMBER() OVER () AS rn,
        t.code, t.name, t.title, t.wdate
    FROM 
        test t
    """
    cursor.execute(msg2)
    rows = cursor.fetchall()
    

    cnt_msg = "select count(*) cnt from test"
    cursor.execute(cnt_msg)
    cnt_row = cursor.fetchone()
    cnt = cnt_row[0]

    scnt_msg = f"select count(*) cnt from test where {skey} like '%{sval}%'"
    cursor.execute(scnt_msg)
    scnt_row = cursor.fetchone()
    scnt = scnt_row[0]
    connection.close()
    

    result = []
    for data in rows:
        row = {'rn':data[0], 'code':data[1], 'name':data[2], 'title':data[3], 'wdate':data[4].strftime('%Y-%m-%d'), 'rcnt':data[5] } 
        result.append(row)

    if(scnt%10==0):
        pageCount = scnt/10
    else:
        pageCount = (scnt/10)+1

    context = {
        'cnt': cnt,
        'scnt': scnt,
        'startPage': startPage,
        'endPage': endPage,
        'returnpage': returnPage,
        'pageNum': pageNum,
        'pageCount': pageCount,
        'result': result
    }
    return render(request, 'blog/blogselect.html', context)


def blogdetail(request):
    idx = request.GET.get('idx')
    cursor = connection.cursor()

    msg = "select * from test where code = "+ idx
    cursor.execute(msg)
    rows = cursor.fetchall()
    result = []
    for data in rows:
        row = {'code':data[0], 'name':data[1], 'title':data[2], 'wdate':data[3].strftime('%Y-%m-%d') } 
        result.append(row)

    msg2 = f"""select 
                    @rownum:=@rownum+1 as rrn, 
                    r.* 
                from 
                    testreply r, 
                    (select @rownum:=0) B 
                where 
                    rcode = {idx}"""

    cursor.execute(msg2)
    replys = cursor.fetchall()
    connection.commit()
    connection.close()
    results = []
    for data in replys:
        dto = {'rrn':int(data[0]), 'rnum':data[1], 'rwriter':data[2], 'rmemo':data[3], 'rcode':data[4] }
        results.append(dto)
    
    context = {
        'result' : result,
        'results' : results
    }

    return render(request, 'blog/blogdetail.html', context)

def blogdelete(request):
    idx = request.GET.get('idx')
    msg = "delete from test where code = "+ idx
    cursor = connection.cursor()
    cursor.execute(msg)  
    connection.commit()
    connection.close()
    return redirect('blogselect.do')

def blogedit(request):
    idx = request.GET.get('idx')
    msg = "select * from test where code = "+ idx
    cursor = connection.cursor()
    cursor.execute(msg)
    rows = cursor.fetchall()
    connection.commit()
    connection.close()

    result = []
    for data in rows:
        row = {'code':data[0], 'name':data[1], 'title':data[2], 'wdate':data[3] } 
        result.append(row)
    
    return render(request, 'blog/blogedit.html', {'result':result})

def blogeditsave(request):
    
    if request.method == 'GET':
        return redirect('blogselect.do')
    elif request.method == 'POST':
        dcode = request.POST.get('code')
        dname = request.POST.get('name')
        dtitle = request.POST.get('title')

        cursor = connection.cursor()
        msg = "UPDATE test SET name=%s, title=%s WHERE code = %s"        
        cursor.execute(msg, (dname, dtitle, dcode))
        connection.commit()
        connection.close()
        print(dcode, '코드 데이터 수정 성공')

 
    return redirect(f"blogdetail.do?idx={dcode}")

def blogReplySave(request):
    rcode = request.GET.get('idx')
    print(rcode)

    if request.method == 'GET':
        return redirect('blogselect.do')
    elif request.method == 'POST':
        rwriter = request.POST.get('rwriter')
        rmemo = request.POST.get('rmemo')
        rcode = request.POST.get('rcode')

        cursor = connection.cursor()
        msg = f"insert into testreply(rwriter, rmemo, rcode) values('{rwriter}', '{rmemo}', {rcode})"
        cursor.execute(msg)
        connection.commit()
        connection.close()
        print(rcode, '코드 데이터 저장 성공')

    return redirect(f"blogdetail.do?idx={rcode}")

def blogReplyEdit(request):
    pass

def blogReplyEditSave(request):
    if request.method == 'GET':
        return redirect('blogselect.do')
    elif request.method == 'POST':
        rwriter = request.POST.get('rwriter')
        rmemo = request.POST.get('rmemo')
        rnum = request.POST.get('rnum')
        rcode = request.POST.get('rcode')

        cursor = connection.cursor()
        msg = "UPDATE testreply SET rwriter=%s, rmemo=%s WHERE rnum = %s"        
        cursor.execute(msg, (rwriter, rmemo, rnum))
        connection.commit()
        connection.close()       

    return redirect(f"blogdetail.do?idx={rcode}")

def blogReplyDelete(request):
    rcode = request.GET.get('idx')
    rnum = request.GET.get('ridx')
    msg = "delete from testreply where rnum = "+ rnum
    cursor = connection.cursor()
    cursor.execute(msg)  
    connection.commit()
    connection.close()
    return redirect(f"blogdetail.do?idx={rcode}")






