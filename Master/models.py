from django.db import models
from Admin.models import *


class tbl_question(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_content=models.CharField(max_length=500)
    question_score=models.IntegerField()
    option_1=models.CharField(max_length=500)
    option_2=models.CharField(max_length=500)
    option_3=models.CharField(max_length=500)
    option_4=models.CharField(max_length=500)
    answer=models.CharField(max_length=500)
    category_id=models.ForeignKey(tbl_category,on_delete=models.CASCADE)
    answer_key=models.CharField(max_length=500,null=True)