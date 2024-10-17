from django.shortcuts import render
from .models import Transactions
from rest_framework.response import Response 
from .serializers import TransactionSerializer 
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status


@api_view(["GET", "POST"])
def get_transactions(request):
    queryset=Transactions.objects.all().order_by('-pk')
    serializer=TransactionSerializer(queryset,many=True)

    return Response({
         "data" : serializer.data
    })

class TransactionAPI(APIView):
    def get(self,request):
        queryset=Transactions.objects.all().order_by('-pk')
        serializer=TransactionSerializer(queryset,many=True)

        return Response({
         "data" : serializer.data
    })

    def post(self,request):
        data =request.data
        serializer=TransactionSerializer(data=data)
        if not serializer.is_valid():
            return Response({
            "message": "data not saved",
            "errors" :serializer.errors
        })
        serializer.save()
        return Response({
            "message" :"data is saved",
            "data": serializer.data
        })
    def put(self,request,pk):#does full update in all fields . you have to update the whole field like in above field you have to update all title amount and transaction type
        try:
            transaction = Transactions.objects.get(pk=pk)
        except Transactions.DoesNotExist:
            return Response({"message": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "data updated",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "data not updated",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    # this is partial update .if you want to update just one field it allows this.l for eg if you want to update just the amount you can do that.
    def patch(self,request):
        data=request.data
        if not data.get('id'):
            return Response({
            "message": "data not updated",
            "errors" :"id is required"})
        try:
            transaction=Transactions.objects.get(id=data.get("id"))
        except Transactions.DoesNotExist:
            return Response({
            "message": "data not found",
            "errors": "Transaction with this ID does not exist"
        })
        serializer = TransactionSerializer(transaction, data=data, partial=True)

        if not serializer.is_valid():
            return Response({
            "message": "data not saved",
            "errors" :serializer.errors
        })
        serializer.save()
        return Response({
            "message" :"data is saved",
            "data": serializer.data
        })
    def delete(self,request):
        data=request.data
        if not data.get("id"):
            return Response({
                "message":"data not found",
                "error":"id is required"

            })
        transaction= Transactions.objects.get(id= data.get("id")).delete()

        return Response({
            "message":"data deleted",
            "data" :()
        })





'''    class TransactionAPI(APIView):
    def get(self,request):
        return Response({
            "message": "this is get method"
        })
    def post(self,request):
        return Response({
            "message": "this is post method"
        })
    def put(self,request):
        return Response({
            "message": "this is put method"
        })
    def patch(self,request):
        return Response({
            "message": "this is patch method"
        })'''