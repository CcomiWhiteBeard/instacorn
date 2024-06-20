from django.shortcuts import render
from django.shortcuts import redirect
from django.db  import connection 
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import string
import random
import hashlib
import base64

from django.contrib.auth.hashers import pbkdf2


# Create your views here.
def hashing_password(m_pwd):
    count = random.randint(16, 21)
    string_pool = string.ascii_letters + string.digits + string.punctuation
    m_salt = "".join(random.choices(string_pool, k=count))
    hashedpw = hashlib.md5(str(m_pwd + m_salt).encode('utf-8')).hexdigest()

    return m_salt, hashedpw

#로그인
def inslogin(request):
    if request.method=='GET':
        return render(request, 'index.html')
    
    else:
        m_id = request.POST.get('m_id')
        m_pwd = request.POST.get('m_pwd')

        try:
            # auth_user 테이블에서 사용자 인증
            user = authenticate(request, username=m_id, password=m_pwd)
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('/admin/')

            # auth_user 테이블에 없는 경우 insta_member 테이블에서 확인
            cursor = connection.cursor()
            msg = "select m_id, m_pwd, m_salt, m_active from insta_member where m_id = %s"
            cursor.execute(msg, [m_id])
            data = cursor.fetchone()
            
            #아이디가 틀렸을 때
            if not data:
                messages.error(request, '아이디가 존재하지 않습니다')
                return redirect('inslogin.do')

            regid, regpw, m_salt, m_active = data           

            # MD5와 저장된 솔트를 사용하여 비밀번호를 검증
            hashedpw = hashlib.md5(str(m_pwd + m_salt).encode('utf-8')).hexdigest()
            
            if hashedpw != regpw:
                messages.error(request, '비밀번호가 일치하지 않습니다')
                return redirect('inslogin.do')
            
            if not m_active:
                messages.error(request, '계정이 비활성화되었습니다.')
                return render(request, 'instacorn/block.html')
            
            request.session['m_id'] = regid
            return render(request, 'instacorn/main.html')
                
        except Exception as e:
            connection.rollback()
            print('failed login', e)
            messages.error(request, '에러 발생')
            return redirect('inslogin.do')

#def 비밀번호찾기

#def 로그아웃
def inslogout(request):
    pass

#회원가입
def insjoin(request):
    if request.method=='GET':
        return render(request, 'instacorn/insjoin.html')
    
    else:
        m_email = request.POST.get('m_email')
        m_name = request.POST.get('m_name')
        m_id = request.POST.get('m_id')
        m_pwd = request.POST.get('m_pwd')

        try:
            cursor = connection.cursor()
            msg="select m_id from insta_member where m_id = (%s)"
            cursor.execute(msg, (m_id,))
            data = cursor.fetchall()

            if len(data) != 0:
                messages.error(request, '이미 존재하는 아이디입니다. 다른 아이디를 사용해주세요.')
                return redirect('insjoin.do')
            
            else:
                m_salt, hashedpw = hashing_password(m_pwd)
                msg="insert into insta_member(m_id, m_pwd, m_name, m_email, m_salt) values(%s, %s, %s, %s, %s)"
                cursor.execute(msg, (m_id, hashedpw, m_name, m_email, m_salt))

                messages.success(request, '회원가입 완료, 로그인을 해주세요.')
                return redirect('inslogin.do')
                
        except:
            connection.rollback()
            print("회원가입실패")

            messages.error(request, '회원가입 에러 발생')
            return redirect('insjoin.do')
        
        finally:
            connection.close()

#회원정보수정
def insmember_modify(request):
    user=request.user
    if request.method=="POST":
        m_name = request.POST.get('m_name')
        m_id = request.POST.get('m_id')
        
        try:
            # user = User.objects.get(m_name=user.m_name)
            user.m_name = m_name
            user.m_id = m_id
            user.save()

            return redirect('', user.m_name)
        except:
            messages.error(request, "회원정보수정 에러")
            return redirect('insmember_modify.do')
        
    return render(request, 'instacorn/insmember_modify.html', {'user':user})

#비밀번호변경
def inspwd_modify(request):
    if request.method=="GET":
        return render(request, 'instacorn/insmember_modify.html')
    
    else:
        user = request.user
        exist_m_pwd = request.POST.get('exist_m_pwd')
        new_m_pwd = request.POST.get('new_m_pwd')

        if user.check_password(exist_m_pwd):
            user.set_password(new_m_pwd)
            user.save()

            messages.success(request, '비밀번호 변경, 재로그인')
            return redirect('inslogin.do')
        else:
            messages.error(request, '현재 비밀번호가 틀렸습니다. 다시 입력해주세요.')
            return redirect('inspwd_modify.do')





