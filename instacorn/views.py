from django.shortcuts import render, redirect
from django.http  import HttpResponse
from django.db  import connection 
from django.core.files.storage import FileSystemStorage  
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


# rcode값 idx값 확인 완료
def insdetail(request):
    idx = request.GET.get('idx')
    print('idx =', idx)
    msg = "select * from insta_board where b_code = " + idx
    cursor = connection.cursor()
    cursor.execute(msg)
    rows = cursor.fetchall()
    print(rows)

    result = []
    for data in rows:
        row = {'b_code':data[0], 'b_content':data[1], 'b_photo':data[2], 'b_no':data[3], 'b_date':data[4], 'b_active':data[5]}
        result.append(row)
        print(row)

    rmsg = "select * from insta_reply where r_code = " + idx 
    cursor = connection.cursor()
    cursor.execute(rmsg)
    rows = cursor.fetchall()
    connection.commit()
    connection.close()

    rresult = []
    for data in rows:
        row = {'r_num':data[0], 'r_content':data[1], 'r_date':data[2], 'r_no':data[3], 'r_code':data[4]}
        rresult.append(row)


    print('result :', result, '\nrresult :', rresult)
    print()
    return render(request, 'instacorn/insdetail.html', {'result':result, 'rresult':rresult, 'idx':idx, 'MEDIA_URL': settings.MEDIA_URL}) 

# 게시물 삭제 완료
def insdelete(request):
    print('insdelete(request) method : 삭제')

    idx = request.GET.get('idx')
    print('idx =', idx)
    msg = "delete from insta_board where b_code = " + idx
    print(msg)
    cursor = connection.cursor()
    cursor.execute(msg)
    connection.commit()
    connection.close()

    return redirect('insdetail.do?idx='+idx)

# 게시물 내용 수정
def insupdate(request):
    print('insupdate(request) method : 수정 화면 들어가기')

    idx = request.GET.get('idx')
    print('idx =', idx)
    cursor = connection.cursor()
    msg = "select * from insta_board where b_code = " + idx
    cursor.execute(msg)
    rows = cursor.fetchone()
    connection.commit()
    connection.close()

    b_content = rows[1]

    return render(request, 'instacorn/insupdate.html', {'idx':idx, 'b_content':b_content})

def insupdatesave(request):
    print('insupdatesave(request) method : 수정 완료')

    if request.method == 'GET':
        return render(request, 'instacorn/insupdatesave.html')
    elif request.method == 'POST':
        idx = request.POST.get('idx')
        print('idx =', idx)
        b_content = request.POST.get('b_content')
        cursor = connection.cursor()
        msg = f"update insta_board set b_content = '{b_content}' where b_code = " + idx
        cursor.execute(msg)
        connection.commit()
        connection.close()
        print('코드 수정 완료 b_content =', b_content)
    
    return HttpResponse('<script>window.close();</script>')
    # return redirect('insdetail.do?idx='+idx)


def insreplyinsert(request):
    print('ins어플 insreplyinsert(request) method : 댓글 등록')

    if request.method == 'GET':
        return render(request, 'instacorn/insreplyinsert.html')
    elif request.method == 'POST':
        r_content = request.POST.get('r_content')
        r_no = request.POST.get('r_no')
        r_code = request.POST.get('r_code')
        print('r_no', r_no)

        cursor = connection.cursor()
        msg = f"insert into insta_reply (r_content, r_no, r_code) values('{r_content}', '{r_no}', '{r_code}')"
        cursor.execute(msg)
        connection.commit()
        connection.close() 

    return redirect('insdetail.do?idx=' + r_code)

def insreplyupdate(request):
    print('ins어플 insreplyupdate(request) method : 댓글 수정')

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        r_num = request.POST.get('r_num')
        r_content = request.POST.get('r_content')
        r_code = request.POST.get('r_code')

        cursor = connection.cursor()
        msg = f"update insta_reply set r_content = '{r_content}' where r_num = {r_num}"
        cursor.execute(msg)
        connection.commit()
        connection.close()
        print(r_num, ': 댓글 수정 완료')
        print('rcode확인', r_code)

    return redirect('insdetail.do?idx=' + r_code)

def insreplydelete(request):
    print('ins어플 insreplydelete(request) method : 댓글 삭제')

    idx = request.GET.get('idx')
    print('idx =', idx)

    ridx = request.GET.get('ridx')
    print('ridx =', ridx)

    msg = "delete from insta_reply where r_num = " + ridx
    cursor = connection.cursor()
    cursor.execute(msg)
    connection.commit()
    connection.close()

    return redirect('insdetail.do?idx='+idx)