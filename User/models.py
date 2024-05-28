from django.db import models
from Guest.models import *
from Master.models import *

class tbl_test(models.Model):
    test_id = models.AutoField(primary_key=True)
    test_date=models.DateField(auto_now_add=True)
    test_start_time=models.TimeField(auto_now_add=True)
    test_end_time=models.CharField(max_length=100,default=0)
    test_score=models.CharField(max_length=100,default=0)
    test_status=models.CharField(max_length=25,default=0)
    user_id = models.ForeignKey(tbl_user,on_delete=models.CASCADE)

class tbl_test_question(models.Model):
    test_question_id = models.AutoField(primary_key=True)
    test_question_answer=models.CharField(max_length=100,null=True)
    question_id=models.ForeignKey(tbl_question,on_delete=models.CASCADE)
    test_id=models.ForeignKey(tbl_test,on_delete=models.CASCADE)
    test_question_score=models.CharField(max_length=100)
