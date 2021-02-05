from django.db import models

# Create your models here.
class Webdata(models.Model):
    webdata_id = models.AutoField
    webdata_name = models.CharField(max_length=100)
    webdata_list = models.TextField(null=True)