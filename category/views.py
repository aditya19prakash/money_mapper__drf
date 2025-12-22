from rest_framework.views import APIView
from transaction.models import Transaction
from django.db.models import Sum
from category.serializer import Category_Serializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
class Categorized(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = Category_Serializer
    def get(self,request):
        queryset = Transaction.objects.filter(user_id=request.user.id).values(
        "category").annotate(credits = Sum("credit"),debits = Sum("debit"))
        serializer = self.serializer_class(queryset,many=True)
        return Response(serializer.data,status=200)



        
