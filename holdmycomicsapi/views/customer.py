# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from holdmycomicsapi.models import Customer, User

class CustomerView(ViewSet):
    """HMC Customers View"""
    
    def create(self, request):
        """POST Customer"""
        
        store_id = User.objects.get(pk=request.data["storeId"])
        customer = Customer.objects.create(
            store_id = store_id,
            customer_name=request.data["customerName"],
            email=request.data["email"],
        )
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk):
        """GET Single Customer"""
        
        customer = Customer.objects.get(pk=pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def list(self, request):
        """GET All Customers"""

        customers = Customer.objects.all()
        store_id = request.query_params.get('storeId', None)
        if store_id is not None:
            customers = customers.filter(store_id=store_id)
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk):
        """PUT Customer"""
        
        customer = Customer.objects.get(pk=pk)
        customer.store_id = User.objects.get(pk=request.data["storeId"])
        customer.customer_name = request.data["customer_name"]
        customer.email = request.data["email"]
        customer.save()
        return Response('Customer Updated', status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        """DELETE Customer"""
        
        customer = Customer.objects.get(pk=pk)
        customer.delete()
        return Response('Customer Deleted', status=status.HTTP_204_NO_CONTENT)
      
class CustomerSerializer(serializers.ModelSerializer):
    """JSON Serializer for Customers"""
  
    class Meta:
        model = Customer
        fields = ('id', 'store_id', 'customer_name', 'email')
