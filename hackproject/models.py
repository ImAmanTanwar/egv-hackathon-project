from django.db import models

# Create your models here.
class Categories(models.Model):
    c_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100,null=True,blank=True,default="")
    desc = models.CharField(max_length=100,null=True,blank=True,default="")

    def __str__(self):
        return str(self.c_id)

class SubCategories(models.Model):
    s_id = models.CharField(max_length=100)
    service_name = models.CharField(max_length=100,null=True,blank=True,default="")
    service_code = models.CharField(max_length=100,null=True,blank=True,default="")
    desc = models.CharField(max_length=100,null=True,blank=True,default="")
    metadata = models.CharField(max_length=100,null=True,blank=True,default="")
    s_type = models.CharField(max_length=100,null=True,blank=True,default="")
    keywords = models.CharField(max_length=100,null=True,blank=True,default="")
    group_id = models.ForeignKey(Categories)
    sla_hours = models.CharField(max_length=100,null=True,blank=True,default="")

    def __str__(self):
        return str(self.s_id)

class Complains(models.Model):
    user_id = models.CharField(max_length=100,null=True,blank=True,default="")
    user_name =  models.CharField(max_length=100,null=True,blank=True,default="")
    mobile_no =  models.CharField(max_length=100,null=True,blank=True,default="")
    service_code = models.CharField(max_length=100,null=True,blank=True,default="")
    lat =  models.CharField(max_length=100,null=True,blank=True,default="")
    lon =  models.CharField(max_length=100,null=True,blank=True,default="")
    tweet =  models.CharField(max_length=160,null=True,blank=True,default="")
