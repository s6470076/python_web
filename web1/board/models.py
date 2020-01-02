from django.db import models

# Create your models here.

class Table1(models.Model):
    object = models.Manager()

    no     = models.AutoField(primary_key=True)
    title  = models.CharField(max_length=200)
    content= models.TextField()
    writer = models.CharField(max_length=50)
    hit    = models.IntegerField()
    img    = models.BinaryField(null=True)
    regdate= models.DateTimeField(auto_now_add=True)