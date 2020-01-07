from django.db import models


class Table2(models.Model):
    objects = models.Manager()

    no        = models.AutoField(primary_key=True)
    name      = models.CharField(max_length=30)
    kor       =  models.IntegerField()
    eng       = models.IntegerField()
    math      = models.IntegerField()
    classroom = models.CharField(max_length=3)
    regdate   = models.DateTimeField(auto_now_add=True)