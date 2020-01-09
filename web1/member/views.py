from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.contrib.auth.models import User 
from django.contrib.auth import login as login1
from django.contrib.auth import logout as logout1 
from django.contrib.auth import authenticate as auth1

from .models import Table2
from django.db.models import Sum, Max, Min, Count, Avg
import pandas as pd

import matplotlib.pyplot as plt
import io #byte로 변환
import base64 #byte를 base64로 변경
from matplotlib import font_manager, rc #한글 폰트 적용

cursor=connection.cursor()

def graph(request):
    # SELECT SUM("kor") FROM MEMBER_TABLE2
    sum_kor = Table2.objects.aggregate(Sum("kor"))
    print("=============================================")
    print(sum_kor) #{"kor__sum":3078}
    print("=============================================")

    # SELECT SUM("kor") AS sum1 FROM MEMBER_TABLE2
    sum_kor = Table2.objects.aggregate(sum1=Sum("kor"))
    print("=============================================")
    print(sum_kor) # {'sum1': 3078}
    print("=============================================")

    # SELECT SUM("kor") FROM MEMBER_TABLE2 
    # WHERE CLASSROOM=102
    sum_kor = Table2.objects.filter(classroom='2') \
        .aggregate(sum1=Sum("kor")) #{'sum1':34}
    print(sum_kor)

    # SELECT SUM("kor") FROM MEMBER_TABLE2
    # WHERE KOR > 10
    # > gt, >= gte,  < lt,   <= lte
    sum_kor = Table2.objects.filter(kor__gt=10) \
        .aggregate(sum1=Sum("kor"))
    print(sum_kor)

    # 반별 합계
    # SELECT SUM("kor") sum1, SUM("eng") sum2, 
    #       SUM("math") sum3
    # FROM MEMBER_TABLE2
    # GROUP BY CLASSROOM
    sum_kor = Table2.objects.values("classroom") \
        .annotate(sum1=Sum("kor"), sum2=Sum('eng'), sum3=Sum('math'), avg1=Avg("kor"))
 
    print(sum_kor) 
    print(sum_kor[0]['sum1'])   
    print(sum_kor.query) #SQL문 확인 

    #-----------------------------------------------------------내가 만든 부분
    avg_kor = Table2.objects.aggregate(avg1= Avg("kor"))
    print(avg_kor['avg1'])
 

    avg_kor = Table2.objects.values("classroom").annotate(avg1= Avg("kor"))
    print(avg_kor)
    print(avg_kor[0]['avg1'])
    print(Table2.objects.values('classroom')) 
    print(avg_kor.query)    
    #-----------------------------------------------------------    

    df = pd.DataFrame(sum_kor)
    df = df.set_index("classroom")
    print(df)
    print(df.columns)
    df.plot(kind="bar")


    '''
    x = ['kor', 'eng', 'math']
    y = [45,   3,  4]

    # 폰트 읽기
    font_name = font_manager \
        .FontProperties(fname="c:/Windows/Fonts/malgun.ttf") \
        .get_name()
    '''
    # # 폰트 적용    
    # rc('font', family=font_name)     

    # plt.bar(x,y)
    # plt.title("AGES & PERSON")
    # plt.xlabel("나이")
    # plt.ylabel("숫자")

    #plt.show()  #표시
    plt.draw()  #안보이게 그림을 캡쳐
    img = io.BytesIO() # img에 byte배열로 보관
    plt.savefig(img, format="png") #png파일 포멧으로 저장
    img_url = base64.b64encode(img.getvalue()).decode()    

  
    plt.close()    #그래프 종료


    return render(request, 'member/graph.html',
        {"graph1":'data:;base64,{}'.format(img_url)})
    # <img src="{{graph1}}" />  <=  graph.html에서


def dataframe(request): 
    #1.Queryset -> list로 변경
    #SELECT * FROM MEMBER_TABLE2(다 가져오겠다), #SELECT NO, NAME, KOR FROM MEMBER_TABLE2(내가 지정한 것만 가져오겠다)
    rows = list(Table2.objects.all().values('no','name','kor'))[0:10]
    print(rows)
    
    #2.list -> dataframe으로 변경
    df = pd.DataFrame(rows)
    print(df)
    
    #3.dataframe -> list
    rows1 = df.values.tolist() 
    
    return render(request,'member/dataframe.html', {'df_table':df.to_html(),'list':rows1})


    


def js_index(request):
    return render(request,'member/js_index.html')

def js_chart(request):
    
    return render(request,'member/js_chart.html')
        



def exam_insert(request):
    for i in range(20):
        obj = Table2()
        obj.name = '마바사'+i
        obj.kor = 80
        obj.eng = 60
        obj.math = 96
        obj.classroom = 104
        obj.save()
        
def exam_select(request):
    txt  = request.GET.get('txt','')
    page = int(request.GET.get("page",1)) #웹페이지가 안 들어오면 1페이지가 표시된다. 0인 페인지는 없으니까 1
    # 1 =>  1, 10
    # 2 => 11, 20
    # 3 => 21, 30
    if txt == "": #검색어가 없는 경우 전체 출력
        #select * FROM MEMBER_TABLE2
        list = Table2.objects.all()[(page*10)-10 : page*10] #슬라이싱으로 해석해라
        
        #select count(*) FROM MEMBER_TABLE2
        cnt  = Table2.objects.all().count() 
        tot  = (cnt-1)//10+1
        # 10 => 1
        # 13 => 2
        # 20 => 2
        # 31 => 4
    
    else : #검색어가 있는 경우
        #select * FROM MT2 WHERE name LIKE '%가%'
        list = Table2.objects.all().filter(name__contains=txt)[page*10-10:page*10]
        
        #select count(*) FROM MT2 WHERE name LIKE '%가%'
        cnt  = Table2.objects.all().filter(name__contains=txt).count() 
        tot  = (cnt-1)//10+1
    
    
    return render(request,"member/exam_select.html",
    {'list':list, 'pages':range(1,tot+1,1)})


    
    # SELECT SUM(math) FROM MEMBER_TABLE2 WHERE CLASS_ROOM=101
    #list = Table2.objects.aggregate(Sum('math'))

    # SELECT NO, NAME FROM MEMBER_TABLE2
    #list = Table2.objects.all().values('no','name')

    # SELECT * FROM MEMBER_TABLE2 ORDER BY name ASC
    #list = Table2.objects.all().order_by('name')
    #list = Table2.objects.raw("SELECT * FROM MEMBER_TABLE2 ORDER BY name ASC")

    # 반별 국어, 영어, 수학 합계
    # SELECT SUM(kor) AS kor, SUM(eng) AS eng, SUM(math) AS math FROM MEMBER_TABLE2 GROUP BY CLASSROOM
    #list = Table2.objects.values('classroom').annotate(kor=Sum('kor'),eng=Sum('eng'),math=Sum('math'))   
    
    #return render(request, 'member/exam_select.html',{"list":list}) 


# -> 작성하려면 -> 화면생각 ->views-> 함수 틀 -> render-> urls.py -> views
'''
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
 
 
 
##########################################################################
    elif request.method == "POST":

        
        obj = Table2()
        obj.name = request.POST["name"]
        obj.kor = request.POST["kor"]
        obj.eng = request.POST["eng"]
        obj.math = request.POST["math"]
        obj.classroom = request.POST["classroom"]
        obj.save()

        
        return redirect("/member/exam_insert")

 ###########################################################################       


def exam_select(request):
    pass

def exam_update(request):
    pass

def exam_delete(request):
    pass

'''



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

def list1(request):
    #ID기준으로 오름차순
    sql = "SELECT * FROM MEMBER ORDER BY ID ASC"
    cursor.execute(sql)
    data = cursor.fetchall()
    print(type(data))#list
    print(data)#[(1,2,3,4),(),(),()]

    #list.html을 표시하기 전에
    #list 변수에 data값을, title변수에 회원목록 문자를
    return render(request, 'member/list1.html',{"list1":data,"title":"회원목록"})
    

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




