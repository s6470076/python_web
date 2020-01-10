#레스트풀 과정
from django.shortcuts import render
from django.http import HttpResponse
from .models import Item
from .serializers import ItemSerializer
from rest_framework.renderers import JSONRenderer
import json
# 127.0.0.1:8000/api/select1?key=abc
# {"id":"a"} => 물품 1개

def select1(request):
    key = request.GET.get('key','')
    num = int(request.GET.get('num','1'))
    search = request.GET.get('search','')
    
    #db에서 확인
    data = json.dumps({"ret":'key error'})

    if key == 'abc':
        obj = Item.objects.filter(name__contains=search)[:num]
        serializer = ItemSerializer(obj, many=True)
        data = JSONRenderer().render(serializer.data)    
       
    
    return HttpResponse(data) 

#[{"id":"a"}, {"id":"b"}] => 물품 여러개
def select2(request):
    obj = Item.objects.all()
    serializer = ItemSerializer(obj, many=True)
    data = JSONRenderer().render(serializer.data)
    return HttpResponse(data) 

def insert1(request):
    for i in range(1,31,1):
        obj = Item()
        obj.name = '아이폰'+str(i)
        obj.price = 1000+i
        obj.save()


    return HttpResponse("insert1")

