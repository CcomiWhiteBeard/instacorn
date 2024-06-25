from django.shortcuts import render, redirect
from django.http  import HttpResponse
from django.db  import connection 
from django.core.files.storage import FileSystemStorage  
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.conf import settings
import datetime

def instest(request):
    context = {
        'boardTable': [
            { 'code': 1200, 'name':'aaa', 'title': 'summer'},
            { 'code': 2400, 'name':'bbb', 'title': 'winter'},
            { 'code': 3500, 'name':'ccc', 'title': 'spring'}
        ] 
    }
    return render(request, 'instacorn/main.html', context)

def home(request):
     # 세션에서 사용자 번호(m_no) 가져오기
    m_no = request.session.get('m_no')
    
    cursor = connection.cursor()
    msg_profile = "SELECT m_id, m_name, m_img FROM insta_member WHERE m_no = %s"
    cursor.execute(msg_profile, [m_no])
    data_profile = cursor.fetchone()
    #result_profile = {'m_id':data_profile[1],'m_name':data_profile[3],'m_img':data_profile[5],}
    result_profile = {'m_id': data_profile[0], 'm_name': data_profile[1], 'm_img': data_profile[2]}

    # insta_board 테이블에서 사용자 게시글 목록 조회
    msg_board = """select b.*, (select m_id from insta_member m where b.b_no = m.m_no), 
    (select m_img from insta_member m where b.b_no = m.m_no), 
    (select count(*) from insta_board_singo bs where b.b_code=bs.bs_code)
    from insta_board b order by b_date desc"""
    cursor.execute(msg_board)
    rows = cursor.fetchall()

    connection.close()
    
    result_board = []
    for data in rows:
        row = {'b_code':data[0],'b_content':data[1],'b_photo':data[2],'b_no':data[3],'b_date':data[4],'b_active':data[5],'user_id':data[6],'user_img':data[7],'b_singo_cnt':data[8]}
        result_board.append(row)
    
    return render(request, 'instacorn/home.html', {'result_profile':result_profile,'result_board':result_board})

def board_singo(request):
    b_code = request.GET.get('b_code')

    cursor = connection.cursor()
    msg = f"insert into insta_board_singo values({b_code})"
    cursor.execute(msg)
    connection.commit()
    connection.close()

    return redirect('/home.do/')

def myprofile(request):
    b_no = request.GET.get('b_no')
    user_no = request.session.get('m_no') #로그인 세션 연결

    cursor = connection.cursor()

    #프로필/팔로우 정보
    msg_profile = f"""select m.*, (select count(*) from insta_board b where m.m_no=b.b_no),
    (select count(follower_no) from follower f where m.m_no=f.following_no),
    (select count(following_no) from follower f where m.m_no=f.follower_no)
    from insta_member m where m_no={b_no}"""
    cursor.execute(msg_profile)
    data_profile = cursor.fetchone()
    
    result_profile = {
        'm_no':data_profile[0],'m_id':data_profile[1],'m_pwd':data_profile[2],'m_name':data_profile[3],
        'm_email':data_profile[4],'m_img':data_profile[5],'m_active':data_profile[6],'b_cnt':data_profile[9],
        'follower_cnt':data_profile[10],'following_cnt':data_profile[11]
        }
    
    #게시판 정보
    msg_board = f"""select b.*, (select count(*) from insta_board_singo bs where b.b_code=bs.bs_code) 
    from insta_board b where b_no={b_no} order by b_date desc"""
    cursor.execute(msg_board)
    rows_board = cursor.fetchall()

    result_board = []
    for data_board in rows_board:
        row = {'b_code':data_board[0],'b_content':data_board[1],'b_photo':data_board[2],'b_no':data_board[3],
               'b_date':data_board[4],'b_active':data_board[5],'b_singo_cnt':data_board[6],}
        result_board.append(row)

    #좋아요 목록
    msg_like = f"""select b_code, b_photo, b_no, b_active, (select count(*) from insta_board_singo bs where b.b_code=bs.bs_code)
    from insta_board b inner join insta_board_like bo 
    on b.b_code=bo.bo_code where bo_no = {b_no}"""
    cursor.execute(msg_like)
    rows_like = cursor.fetchall()

    result_like = []
    for data_like in rows_like:
        row = {'b_code':data_like[0],'b_photo':data_like[1],'b_no':data_like[2],'b_active':data_like[3],'b_singo_cnt':data_like[4],}
        result_like.append(row)

    # 팔로워 목록
    msg_follower = f"""select f.following_no, m_no, m_id, m_name, m_img from insta_member m 
    inner join follower f on f.follower_no=m.m_no where following_no = {b_no}"""
    cursor.execute(msg_follower)
    rows_follower = cursor.fetchall()

    result_follower = []
    for data_follower in rows_follower:
        row = {'following_no':data_follower[0],'m_no':data_follower[1],'m_id':data_follower[2],
               'm_name':data_follower[3],'m_img':data_follower[4],}
        result_follower.append(row)

    # 팔로우 목록
    msg_following = f"""select f.follower_no, m_no, m_id, m_name, m_img from insta_member m 
    inner join follower f on f.following_no=m.m_no where follower_no = {b_no}"""
    cursor.execute(msg_following)
    rows_following = cursor.fetchall()

    result_following = []
    for data_following in rows_following:
        row = {'follower_no':data_following[0],'m_no':data_following[1],'m_id':data_following[2],
               'm_name':data_following[3],'m_img':data_following[4],}
        result_following.append(row)
    
    #팔로우 정보
    msg_followInfo = f"select count(*) from follower where follower_no = 1 and following_no = {b_no}"
    cursor.execute(msg_followInfo)
    followInfo = cursor.fetchone()[0]

    connection.close()

    return render(request, 'instacorn/myprofile.html', 
                  {
                      'result_profile':result_profile, 'result_board':result_board, 'result_follower':result_follower, 
                      'result_following':result_following, 'result_like':result_like, 'user_no': user_no, 'followInfo':followInfo,
                        })

# 팔로워 삭제
def del_follower(request):
    if request.method=='POST':
        follower_no = request.POST.get('follower_no')
        following_no = request.POST.get('following_no')
        cursor = connection.cursor()
        msg_del = f"delete from follower where follower_no = '{follower_no}' and following_no = '{following_no}'"
        cursor.execute(msg_del)
        connection.commit()

        msg_sel = f"""select f.following_no, m_no, m_id, m_name, m_img from insta_member m 
        inner join follower f on f.follower_no=m.m_no where following_no = '{following_no}'"""
        cursor.execute(msg_sel)
        rows_follower = cursor.fetchall()

        result_follower = []
        for data_follower in rows_follower:
            row = {'following_no':data_follower[0],'m_no':data_follower[1],'m_id':data_follower[2],
                'm_name':data_follower[3],'m_img':data_follower[4],}
            result_follower.append(row)

        connection.close()

        return HttpResponse(json.dumps({'result_follower':result_follower}))
    else:
        follower_no = request.GET.get('follower_no')
        following_no = request.GET.get('following_no')
        cursor = connection.cursor()
        msg_del = f"delete from follower where follower_no = '{follower_no}' and following_no = '{following_no}'"
        cursor.execute(msg_del)
        connection.commit()
        connection.close()
        
        return redirect('/myprofile.do/?b_no='+following_no)



#팔로우 취소
def del_following(request):
    if request.method=='POST':
        follower_no = request.POST.get('follower_no')
        following_no = request.POST.get('following_no')
        cursor = connection.cursor()
        msg_del = f"delete from follower where follower_no = '{follower_no}' and following_no = '{following_no}'"
        cursor.execute(msg_del)
        connection.commit()

        msg_sel = f"""select f.follower_no, m_no, m_id, m_name, m_img from insta_member m 
        inner join follower f on f.following_no=m.m_no where follower_no = '{follower_no}'"""
        cursor.execute(msg_sel)
        rows_following = cursor.fetchall()

        result_following = []
        for data_following in rows_following:
            row = {'follower_no':data_following[0],'m_no':data_following[1],'m_id':data_following[2],
                'm_name':data_following[3],'m_img':data_following[4],}
            result_following.append(row)

        connection.close()

        return HttpResponse(json.dumps({'result_following':result_following}))
    
    else:
        follower_no = request.GET.get('follower_no')
        following_no = request.GET.get('following_no')
        cursor = connection.cursor()
        msg_del = f"delete from follower where follower_no = '{follower_no}' and following_no = '{following_no}'"
        cursor.execute(msg_del)
        connection.commit()
        connection.close()

        return redirect('/myprofile.do/?b_no='+following_no)

#팔로우
def follow(request):
    if request.method=='POST':
        follower_no = request.POST.get('follower_no')
        following_no = request.POST.get('following_no')

        cursor = connection.cursor()
        msg_insert = f"insert into follower values('{follower_no}',{following_no})"
        cursor.execute(msg_insert)
        connection.commit()

        connection.close()

        return HttpResponse()
    else:
        follower_no = request.GET.get('follower_no')
        following_no = request.GET.get('following_no')

        cursor = connection.cursor()
        msg_insert = f"insert into follower values('{follower_no}',{following_no})"
        cursor.execute(msg_insert)
        connection.commit()
        connection.close()

        return redirect('/myprofile.do/?b_no='+following_no)
    
#회원 신고
def user_singo(request):
    user_no = request.GET.get('user_no')

    cursor = connection.cursor()
    msg = f"insert into insta_member_singo values('{user_no}')"
    cursor.execute(msg)
    connection.commit()
    connection.close()

    return redirect('/myprofile.do/?b_no='+user_no)

#프로필 이미지 수정
@csrf_exempt
def editImage(request):
    if request.method=='POST':
        fileImg = request.FILES['fileImg'] if 'fileImg' in request.FILES else None
        m_no = request.POST.get('m_no')

        print(f'받아온 값 : {fileImg}, {m_no}')

        if fileImg:
            fs = FileSystemStorage(location='media/images')
            fs.save(fileImg.name, fileImg)
        cursor = connection.cursor()
        msg = f"update insta_member set m_img='{fileImg}' where m_no='{m_no}'"
        cursor.execute(msg)
        connection.commit()
        connection.close()

    return redirect('/myprofile.do/?b_no='+m_no)

#검색탭
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
                    on bh_code = b_code where bh_content like '%{sval}%'
            union
            select m_img, m_id, m_name  from insta_member where m_id like '%{sval}%' or m_name like '%{sval}%'
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


# 상세페이지
def insdetail(request):
    m_no = request.session.get('m_no')
    print('m_no', m_no)

    idx = request.GET.get('idx')
    print('idx =', idx)
    msg = "select b.*, m.* from insta_board b inner join insta_member m on b.b_no = m.m_no where b_code = %s"
    cursor = connection.cursor()
    cursor.execute(msg, [idx])
    rows = cursor.fetchall()

    result = []
    for data in rows:
        row = {'b_code':data[0], 'b_content':data[1], 'b_photo':data[2], 'b_no':data[3], 'b_date':data[4], 
               'b_active':data[5], 'm_id': data[7], 'm_name': data[10], 'm_img': data[12]}
        result.append(row)

    rmsg = "select r.*, m.* from insta_reply r inner join insta_member m on r.r_no = m.m_no where r_code = " + idx 
    cursor = connection.cursor()
    cursor.execute(rmsg)
    rows = cursor.fetchall() 
    connection.commit()
    connection.close()

    rresult = []
    for data in rows:
        row = {'r_num':data[0], 'r_content':data[1], 'r_date':data[2], 'r_no':data[3], 'r_code':data[4],
               'm_no':data[5], 'm_id': data[6], 'm_name': data[9], 'm_img': data[11]}
        rresult.append(row)

    #print('result :', result, '\nrresult :', rresult)
    #print()
    return render(request, 'instacorn/insdetail.html', {'result':result, 'rresult':rresult, 'idx':idx, 'MEDIA_URL': settings.MEDIA_URL, 'm_no':m_no}) 

# 게시물 삭제 완료
def insdelete(request):
    print('insdelete(request) method : 삭제')

    idx = request.GET.get('idx')
    #print('idx =', idx)
    msg = "delete from insta_board where b_code = " + idx
    #print(msg)
    cursor = connection.cursor()
    cursor.execute(msg)
    connection.commit()
    connection.close()

    return redirect('insdetail.do?idx='+idx)

# 게시물 내용 수정
def insupdate(request):
    #print('insupdate(request) method : 수정 화면 들어가기')

    idx = request.GET.get('idx')
    #print('idx =', idx)
    cursor = connection.cursor()
    msg = "select * from insta_board where b_code = " + idx
    cursor.execute(msg)
    rows = cursor.fetchone()
    connection.commit()
    connection.close()

    b_content = rows[1]

    return render(request, 'instacorn/insupdate.html', {'idx':idx, 'b_content':b_content})

def insupdatesave(request):
    #print('insupdatesave(request) method : 수정 완료')

    if request.method == 'GET':
        return render(request, 'instacorn/insupdatesave.html')
    elif request.method == 'POST':
        idx = request.POST.get('idx')
        #print('idx =', idx)
        b_content = request.POST.get('b_content')
        cursor = connection.cursor()
        msg = f"update insta_board set b_content = '{b_content}' where b_code = " + idx
        cursor.execute(msg)
        connection.commit()
        connection.close()
        #print('코드 수정 완료 b_content =', b_content)
    
    # return HttpResponse('<script>window.close();</script>')
    return redirect('insdetail.do?idx='+idx)


def insreplyinsert(request):
    #print('ins어플 insreplyinsert(request) method : 댓글 등록')

    if request.method == 'GET':
        return render(request, 'instacorn/insreplyinsert.html')
    elif request.method == 'POST':
        r_content = request.POST.get('r_content')
        r_no = request.POST.get('r_no')
        r_code = request.POST.get('r_code')
        #print('r_no', r_no)

        cursor = connection.cursor()
        msg = f"insert into insta_reply (r_content, r_no, r_code) values('{r_content}', '{r_no}', '{r_code}')"
        cursor.execute(msg)
        connection.commit()
        connection.close() 

    return redirect('insdetail.do?idx=' + r_code)

def insreplyupdate(request):
    #print('ins어플 insreplyupdate(request) method : 댓글 수정')

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
        #print(r_num, ': 댓글 수정 완료')
        #print('rcode확인', r_code)

    return redirect('insdetail.do?idx=' + r_code)

def insreplydelete(request):
    #print('ins어플 insreplydelete(request) method : 댓글 삭제')

    idx = request.GET.get('idx')
    #print('idx =', idx)

    ridx = request.GET.get('ridx')
    #print('ridx =', ridx)

    msg = "delete from insta_reply where r_num = " + ridx
    cursor = connection.cursor()
    cursor.execute(msg)
    connection.commit()
    connection.close()

    return redirect('insdetail.do?idx='+idx)