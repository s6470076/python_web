from django.urls import path
from . import views

# 127.0.0.1:8000/member/index => index 함수 작동
# 127.0.0.1:8000/member/join
# 127.0.0.1:8000/member/login
urlpatterns = [




     path('index',views.index, name='index'),
     path('join',views.join, name='join'),
     path('login',views.login, name='login'),
     path('logout',views.logout, name='logout'),
     path('list1',views.list1, name='list1'),
     path('edit',views.edit, name='edit'),
     path('delete',views.delete, name='delete'),
     path('join1',views.join1, name='join1'),
     
     path('auth_join',views.auth_join, name='auth_join'),
     path('auth_login',views.auth_login, name='auth_login'),
     path('auth_logout',views.auth_logout, name='auth_logout'),
     path('auth_edit',views.auth_edit, name='auth_edit'),
     path('auth_pw',views.auth_pw, name='auth_pw'),
     path('auth_index',views.auth_index, name='auth_index'),

     path('exam_insert',views.exam_insert, name='exam_insert'),
     path('exam_select',views.exam_select, name='exam_select'),

     path('js_index',views.js_index, name='js_index'),
     path('js_chart',views.js_chart, name='js_chart'),

     path('dataframe',views.dataframe, name='dataframe'),
     path('graph',views.graph, name='graph'),

]
