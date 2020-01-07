from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.contrib.auth.models import User 
from django.contrib.auth import login as login1
from django.contrib.auth import logout as logout1 
from django.contrib.auth import authenticate as auth1

from .models import Table2
cursor=connection.cursor()




# -> 작성하려면 -> 화면생각 ->views-> 함수 틀 -> render-> urls.py -> views
@csrf_exempt
def exam_insert(request):
    if request.method == "GET":
        return render(request,"member/exam_insert.html", {"cnt":range(20)})
    
    elif request.method == "POST":
        na = request.POST.getlist('name[]')
        ko = request.POST.getlist('kor[]')
        en = request.POST.getlist('eng[]')
        ma = request.POST.getlist('math[]')
        classroom = request.POST.getlist('classroom[]')

        objs = []
        for i in range(0, len(na), 1):        
            obj = Table2()
            obj.name = na[i]
            obj.kor = ko[i]
            obj.eng = en[i]
            obj.math = ma[i]
            obj.classroom = classroom[i]
            objs.append(obj)

        Table2.objects.bulk_create(objs)
        return redirect("/member/exam_insert")
 
 
 
'''
    elif request.method == "POST":

        
        obj = Table2()
        obj.name = request.POST["name"]
        obj.kor = request.POST["kor"]
        obj.eng = request.POST["eng"]
        obj.math = request.POST["math"]
        obj.classroom = request.POST["classroom"]
        obj.save()

        
        return redirect("/member/exam_insert")
'''
        


def exam_select(request):
    pass

def exam_update(request):
    pass

def exam_delete(request):
    pass





@csrf_exempt 
def auth_pw(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect("/member/auth_login")
        return render(request,'member/auth_pw.html')
    elif request.method == 'POST':
        pw = request.POST['pw']
        pw1 = request.POST['pw1']
        obj = auth1(request,username=request.user,password=pw)
        if obj:
            obj.set_password(pw1)
            obj.save()
            return redirect("/member/auth_index")
        return redirect('/member/auth_pw')


@csrf_exempt 
def auth_edit(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect("/member/auth_login")              
        obj = User.objects.get(username=request.user)
        return render(request,'member/auth_edit.html',{'obj':obj})
    
    elif request.method == 'POST':
        id = request.POST['username']
        na = request.POST['first_name']
        em = request.POST['email']
        
        obj = User.objects.get(username=id)
        obj.first_name = na
        obj.email = em
        obj.save()
        return redirect('/member/auth_index')


@csrf_exempt 
def auth_logout(request):
    if request.method == 'GET' or request.method == 'POST':
        logout1(request)#세션초기화
        return render(request,'member/auth_login.html')


@csrf_exempt 
def auth_login(request):
    if request.method == 'GET' :
        return render(request,'member/auth_login.html')
    elif request.method == 'POST':
        id = request.POST['username']
        pw = request.POST['password']

        obj = auth1(request, username=id, password=pw)

        if obj: 
            login1(request, obj)
            return redirect("/member/auth_index")

        return redirect("/member/auth_login")

@csrf_exempt 
def auth_index(request):
    if request.method == 'GET' :
        return render(request,'member/auth_index.html')
    


@csrf_exempt 
def auth_join(request):
    if request.method == 'GET' :
        return render(request,'member/auth_join.html')
    elif request.method == 'POST':
        id = request.POST['username']
        pw = request.POST['password']
        na = request.POST['first_name']
        em = request.POST['email']

        obj = User.objects.create_user(
            username=id,
            password=pw,
            first_name=na,
            email=em)

        obj.save()

        return redirect("/member/auth_index")

##############################################################################

@csrf_exempt 
def delete(request):
    if request.method == 'GET' or request.method == 'POST':
        ar = [request.session['userid']]
        sql =  "DELETE FROM MEMBER WHERE ID=%s"
        cursor.execute(sql, ar)

        return redirect("/member/index")
             





@csrf_exempt 
def edit(request):
    if request.method == 'GET' :
        ar = [request.session['userid']]
        sql = """
            SELECT * FROM MEMBER WHERE ID=%s
         """      
        cursor.execute(sql, ar)
        data = cursor.fetchone()   
        print(data)    
        return render(request,"member/edit.html",{"one":data})
    
    elif request.method == 'POST':
        ar = [
            request.POST['name'],
            request.POST['age'],
            request.POST['id']
            ]

        sql = '''        
        UPDATE MEMBER SET NAME=%s, AGE=%s WHERE ID=%s
        '''
        cursor.execute(sql, ar)

        return redirect("/member/index")


@csrf_exempt #post로 값을 전달 받는 곳은 필수 
def join1(request):
    if request.method == 'GET':            
        return render(request,"member/join1.html")

def list(request):
    #ID기준으로 오름차순
    sql = "SELECT * FROM MEMBER ORDER BY ID ASC"
    cursor.execute(sql)
    data = cursor.fetchall()
    print(type(data))#list
    print(data)#[(1,2,3,4),(),(),()]

    #list.html을 표시하기 전에
    #list 변수에 data값을, title변수에 회원목록 문자를
    return render(request, 'member/list.html',{"list":data,"title":"회원목록"})
    

def index(request):
    #return HttpResponse('index page <hr />')
    return render(request,'member/index.html')

@csrf_exempt #post로 값을 전달 받는 곳은 필수 
def join(request):
    if request.method == 'GET':            
        return render(request,"member/join.html")
    elif request.method == 'POST':
        id = request.POST['id']#html에서 넘어오는 값을 받음
        na = request.POST['name']
        ag = request.POST['age']
        pw = request.POST['pw']

        ar = [id,na,ag,pw] #list로 만듬
        print(ar)
        #DB에 추가
        cursor = connection.cursor()
        sql = """
            INSERT INTO MEMBER(ID,NAME,AGE,PW,JOINDATE)
            VALUES(%s,%s,%s,%s,SYSDATE)
            """
        cursor.execute(sql,ar)
        
        return redirect('/member/index')

@csrf_exempt
def login(request):
    if request.method == 'GET':            
        return render(request,"member/login.html")
    elif request.method == 'POST':  
        ar = [request.POST['id'], request.POST['pw']]
        sql = """
            SELECT ID, NAME FROM MEMBER 
            WHERE ID=%s AND PW=%s
            """
        cursor.execute(sql, ar)
        data = cursor.fetchone()
        print(type(data))
        print(data)

        if data:
            request.session['userid']=data[0]
            request.session['username']=data[1]
            return redirect('/member/index')
        
        return redirect('/member/login')


def logout(request):
    if request.method=='GET' or request.method=='POST':
        del request.session['userid']
        del request.session['username']
        return redirect('/member/index')




