from django.utils.dateparse import parse_date
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from transaction.serializer import FileUploadSerializer,Transaction_serializer,Transaction_View_serializer
from transaction.transc_method import Excel_cleaning
from transaction.models import Transaction
from rest_framework.pagination import PageNumberPagination

class TransactionPagination(PageNumberPagination):
      page_size = 50
      max_page_size = 50
      page_size_query_param = 'size'
      
class Send_bank_Statement(APIView):
      parser_classes = (MultiPartParser, FormParser)
      serializer_class = FileUploadSerializer

      def post(self,request,id):
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=400)
            data = Excel_cleaning.clean(request.data["file"],id)
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
      serializer_class = Transaction_View_serializer
      def get(self,request,id):
            queryset = Transaction.objects.filter(user_id = id)
            date = request.query_params.get("date")
            start  = request.query_params.get("from")
            end  = request.query_params.get("to")
            name = request.query_params.get("name")
            credit_from  = request.query_params.get("credit_from")
            credit_to  = request.query_params.get("credit_to")
            debit_from =  request.query_params.get("debit_from")
            debit_to  = request.query_params.get("debit_to")
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
                  queryset = queryset.filter(credit__range = (credit_from,credit_to),credit__isnull = False)
            if debit_from and debit_to:
                  debit_from = int(debit_from)
                  debit_to = int(debit_to)
                  if not isinstance(debit_from,int) or not isinstance(debit_to,int):
                       return Response({"message":"Invalid format credit"},status=400)
                  queryset = queryset.filter(debit__range = (debit_from,debit_to),debit__isnull = False)
            if name:
                  queryset = queryset.filter(account_name__icontains = name)
            if not queryset.exists():
                  return Response({"message": f"Transaction not found"},
                  status=status.HTTP_404_NOT_FOUND)
            queryset= queryset.filter().order_by("txn_date")
            paginator = TransactionPagination()
            paginted_data = paginator.paginate_queryset(queryset,request)
            serializer = self.serializer_class(paginted_data,many=True)
            return paginator.get_paginated_response(serializer.data)

class view_transaction_id(APIView):
      serializer_class = Transaction_View_serializer
      def get(self,request,id,t_id):
          try:
            data = Transaction.objects.get(user = id,id = t_id,)
            serializer = self.serializer_class(data)
            return Response(serializer.data,status=200)
          except:
            return Response({"message":"Transaction not found"},status=400)
      

      def put(self,requset,id,t_id):
            transaction = Transaction.objects.get(user=id, id=t_id)
            data = requset.data.copy()
            serializer = self.serializer_class(instance=transaction,data=data,partial=True)
            if serializer.is_valid():
               
               serializer.save()
               return Response(serializer.data,status=200)
            return Response(serializer.errors,status=400)
           
           

          
