from django.urls import path
from . import views

urlpatterns = [
    path('list', views.list, name='list'),
    path('write', views.write, name='write'),
    path('edit', views.edit, name='edit'),
    path('delete', views.delete, name='delete'),
    path('content', views.content, name='content'),
    path('dataframe', views.dataframe, name='dataframe')

]
  





