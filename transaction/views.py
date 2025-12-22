from django.utils.dateparse import parse_date
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from transaction.serializer import FileUploadSerializer,Transaction_serializer,Transaction_View_serializer
from transaction.transc_method import Excel_cleaning
from transaction.models import Transaction
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated 
from rest_framework_simplejwt.authentication import JWTAuthentication



class TransactionPagination(PageNumberPagination):
      page_size = 50
      max_page_size = 50
      page_size_query_param = 'size'
      
class Send_bank_Statement(APIView):
      permission_classes = [IsAuthenticated]
      authentication_classes = [JWTAuthentication]
      parser_classes = (MultiPartParser, FormParser)
      serializer_class = FileUploadSerializer
      def post(self,request):
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=400)
            data = Excel_cleaning.clean(request.data["file"],request.user.id)
            failed =0 
            objects = []
            for i in data:
                  save_serializer = Transaction_serializer(data=i)
                  if save_serializer.is_valid():
                        objects.append(Transaction(**save_serializer.validated_data))
                  else:
                        failed+=1
            try:
                  Transaction.objects.bulk_create(objects)  
                  return Response(
                  {
                      "message": "File received successfully",
                      "filename": request.data["file"].name,
                      "Tranaction count":len(data),
                      "saved":len(data)-failed,
                      "Not saved":failed,
                  },
                  status=201
                  )
            except:
                  return Response({"message":"No transaction saved"},status=400)
            
      
class View_transaction(APIView):
      authentication_classes = [JWTAuthentication]
      permission_classes = [IsAuthenticated]
      serializer_class = Transaction_View_serializer
      def get(self,request):
            queryset = Transaction.objects.filter(user_id = request.user.id)
            cache_key = f"transaction:{request.get_full_path()}"
            cache_response = cache.get(cache_key)
            if cache_response:
                 return Response(cache_response,status=200)
            
            date = request.query_params.get("date")
            start  = request.query_params.get("from")
            end  = request.query_params.get("to")
            name = request.query_params.get("name")
            credit_from  = request.query_params.get("credit_from")
            credit_to  = request.query_params.get("credit_to")
            debit_from =  request.query_params.get("debit_from")
            debit_to  = request.query_params.get("debit_to")
            month = request.query_params.get("month")

            if credit_from and credit_to and debit_from and debit_to:
                  return Response(
                         {"message": "Use either credit range or debit range, not both."},
                         status=status.HTTP_400_BAD_REQUEST
                  )
            if date and start and end:
                 return  Response({"message": "Use either 'date' OR ('from' and 'to'), not both."},status=status.HTTP_400_BAD_REQUEST)
            if date:
                  date = parse_date(date)
                  if date is None:
                       return Response({"message":"Invalid date format"},status=400)
                  queryset= queryset.filter(txn_date=date)
            if start and end :
                  start = parse_date(start)
                  end = parse_date(end)
                  if start is None or end is None:
                       return Response({"message":"Invalid date format"},status=400)
                  if start > end:
                       return Response({"message": "'from' date cannot be greater than 'to' date"},status=400)
                  queryset = queryset.filter(txn_date__range = (start,end))       
            if credit_from and credit_to:
                  credit_from = int(credit_from)
                  credit_to = int(credit_to)
                  if not isinstance(credit_from,int) or not isinstance(credit_to,int):
                       return Response({"message":"Invalid format credit"},status=400)
                  queryset = queryset.filter(credit__range = (credit_from,credit_to))
            if debit_from and debit_to:
                  debit_from = int(debit_from)
                  debit_to = int(debit_to)
                  if not isinstance(debit_from,int) or not isinstance(debit_to,int):
                       return Response({"message":"Invalid format credit"},status=400)
                  queryset = queryset.filter(debit__range = (debit_from,debit_to))
            if name:
                  queryset = queryset.filter(account_name__icontains = name)
            if month:
                  month = int(month)
                  if month > 12 or  month < 0:
                        return Response({"message":"Invalid value month"},status=400)
                  queryset = queryset.filter(txn_date__month=month)
            queryset= queryset.filter().order_by("txn_date")
            paginator = TransactionPagination()
            paginated_data = paginator.paginate_queryset(queryset,request)
            if not paginated_data:
                 return Response({"message": "Transaction not found"}, status=404)
            serializer = self.serializer_class(paginated_data,many=True)
            paginated_response = paginator.get_paginated_response(serializer.data).data
            cache.set(cache_key,paginated_response,timeout=60*60)
            return Response(paginated_response,status=201)

class view_transaction_id(APIView):
      serializer_class = Transaction_View_serializer
      def get(self,request,t_id):
            cache_key = f"transaction_id:{request.get_full_path()}"
            cache_response = cache.get(cache_key)
            if cache_response:
                 return Response(cache_response,status=200)
            result = None
            try:
                  data = Transaction.objects.get(user_id = request.user.id,id = t_id,)
                  serializer = self.serializer_class(data)
                  result = serializer.data
            except:
                  result = {"message":"Transaction not found"}
            cache.set(cache_key,result,timeout=60*60)
            return Response(result,status=201)
      

      def put(self,requset,id,t_id):
            transaction = Transaction.objects.get(user=id, id=t_id)
            data = requset.data.copy()
            serializer = self.serializer_class(instance=transaction,data=data,partial=True)
            if serializer.is_valid():
               
               serializer.save()
               return Response(serializer.data,status=200)
            return Response(serializer.errors,status=400)