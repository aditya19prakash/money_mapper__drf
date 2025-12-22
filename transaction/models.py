from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
   id = models.BigIntegerField(primary_key=True)
   user = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
   account_name = models.CharField(max_length=100)
   category = models.CharField(max_length=100,default="uncatogrized")
   credit = models.IntegerField(null=True)
   debit = models.IntegerField(null= True)
   txn_date = models.DateField(null= False)
   description = models.TextField(null= True)
   payment_method = models.CharField(max_length=50)
  


