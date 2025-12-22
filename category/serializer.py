from rest_framework import serializers
from transaction.models import Transaction
class Category_Serializer(serializers.Serializer):
    category = serializers.CharField()
    credits = serializers.IntegerField()
    debits = serializers.IntegerField()
    
  