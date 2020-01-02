from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

cursor = connection.cursor()#sql문 수행위한 cursor 객체




@csrf_exempt  
def content(request):
    if request.method == 'GET': #GET은 주소로 찾아간다 ?기준
        no = request.GET.get('no', 0)  
        # request.GET['no']
        if no == 0 :
            return redirect("/board/list") # <a href와 같음
        if request.session['hit'] == 1:
        #조회수 1증가 시킴
            sql='''
                UPDATE BOARD_TABLE1 SET HIT=HIT+1
                WHERE NO = %s

            '''
            cursor.execute(sql, [no])
            request.session['hit'] = 0
        
        
        sql = """
            SELECT 
                NO, TITLE,CONTENT, WRITER, 
                HIT, 
                TO_CHAR(REGDATE, 'YYYY-MM-DD HH:MI:SS') 
            FROM 
                BOARD_TABLE1
            WHERE
                NO = %s
        """
        cursor.execute(sql, [no])
        data = cursor.fetchone()  # (1,2,3,4,5,6)
        print(no)
        return render(request, 'board/content.html',
             {"one":data}) 



@csrf_exempt 
def list(request):
    if request.method == 'GET':
        request.session['hit'] = 1 
        sql = """SELECT NO, TITLE, WRITER, HIT, TO_CHAR(REGDATE,'YYYY-MM-DD HH:MI:SS') 
                FROM BOARD_TABLE1
                ORDER BY NO DESC
                """
        cursor.execute(sql)
        data = cursor.fetchall()
        print( type(data) ) 
        print(data)  #[(  ),(  )]
        return render(request, "board/list.html",{"list":data})



@csrf_exempt 
def write(request):
    if request.method == 'GET':
        return render(request, "board/write.html")
    elif request.method == "POST":
        img = request.FILES['img'] #name값 img
        arr = [
            request.POST['title'],
            request.POST['content'],
            request.POST['writer'],
            img.read() #이미지를 byte[]로 변경
        ]
        try :
            #print (arr)
            sql = """
                INSERT INTO BOARD_TABLE1(TITLE, CONTENT, WRITER, IMG, HIT, REGDATE)
                VALUES(%s,%s,%s,%s, 234, SYSDATE)
            """
            cursor.execute(sql,arr)
        
        except Exception as e:
            print (e)
        
        return redirect("/board/list")  #<a href와 같음