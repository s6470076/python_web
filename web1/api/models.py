from django.db import models

#python manage.py check
#python manage.py makemigration
#python manage.py migrate

class Item(models.Model):
    objects = models.Manager()

    no        = models.AutoField(primary_key=True)
    name      = models.CharField(max_length=30)
    price     =  models.IntegerField()
    regdate   = models.DateTimeField(auto_now_add=True)

