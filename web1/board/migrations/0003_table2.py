# Generated by Django 2.2.5 on 2020-01-06 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_table1_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='Table2',
            fields=[
                ('no', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('kor', models.IntegerField()),
                ('eng', models.IntegerField()),
                ('math', models.IntegerField()),
                ('regdate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
