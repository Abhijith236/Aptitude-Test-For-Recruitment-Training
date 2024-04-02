from django.db import models
from Admin.models import *


class tbl_master(models.Model):
    master_id = models.AutoField(primary_key=True)
    master_name=models.CharField(max_length=25)
    master_contact=models.IntegerField()
    master_email=models.EmailField()
    master_photo=models.FileField(upload_to="Files/", null=True)
    master_password=models.CharField(max_length=25)


class tbl_user(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name=models.CharField(max_length=25)
    user_contact=models.IntegerField()
    user_email=models.EmailField()
    user_address=models.CharField(max_length=25)
    place_id=models.ForeignKey(tbl_place,on_delete=models.CASCADE)
    user_photo=models.FileField(upload_to="Files/", null=True)
    user_proof=models.FileField(upload_to="Files/", null=True)
    user_password=models.CharField(max_length=25)
    user_status=models.CharField(max_length=25,default=0)