from django.shortcuts import render, redirect
from django.http  import HttpResponse
from django.db  import connection 
from django.core.files.storage import FileSystemStorage  
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import datetime
import time

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

def instaselect(request):
    print('instaselect(request): 검색결과 출력 !!!!!!!!!!!!!!!!!!!!!!!!!!!')
    dt = datetime.datetime.now()

    #검색어
    sval = request.GET.get('sval')
    print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', sval)
    if(sval == "" or sval == None):
        sval = ''

    print('sval 값' + sval)
    # select m_id, m_img, m_name, bh_content  
    # from (select * from insta_member m inner join insta_board b where m.m_no = b.b_no) mb inner join insta_board_hash h 
    # where bh_code = b_code and bh_content like '%홍%';


    hashresult = []
    justresult = []
    cursor = connection.cursor()
    if '#' in sval :
        msg = f"""
            select bh_content  
                from (select * from insta_member m inner join insta_board b where m.m_no = b.b_no) mb inner join insta_board_hash h  
                    where bh_code = b_code and bh_content like '%{sval}%'  
            """
        print(msg)
        
        cursor.execute(msg)
        rows = cursor.fetchall()

        for data in rows:
            row = {'content': data[0]}
            hashresult.append(row)
    else: 
        msg = f"""
            select m_img, m_id, m_name from 
                (select * from insta_member m inner join insta_board b on m.m_no = b.b_no) mb inner join insta_board_hash h  
                    on bh_code = b_code where bh_content like '%{sval}%' or m_id like '%{sval}%' or m_name like '%{sval}%'
            """
        print(msg)

        cursor = connection.cursor()
        cursor.execute(msg)
        print(cursor.execute(msg))
        rows = cursor.fetchall()
        print(rows)
        for data in rows:
            row = {'profileimg': data[0], 'id': data[1], 'name': data[2]}
            justresult.append(row)
            
    print('hashresult값', hashresult )
    print('justresult값', justresult )
    myresult = { 'hashresult': hashresult, 'justresult': justresult }


    return JsonResponse(myresult, safe=False)     #딕션너리 이외의 형식도 받아들임


def instahome(request):
    print('instacorn어플 instahome(request): 인스타 홈')

    return render(request, 'instacorn/instahome.html')