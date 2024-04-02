from django.db import models

class tbl_admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_email = models.CharField(max_length=50)
    admin_password = models.CharField(max_length=50)

class tbl_category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)


class tbl_district(models.Model):
    district_id = models.AutoField(primary_key=True)
    district_name = models.CharField(max_length=50)

class tbl_place(models.Model):
    place_id = models.AutoField(primary_key=True)
    place_name = models.CharField(max_length=50)
    district_id = models.ForeignKey(tbl_district,on_delete=models.CASCADE)
