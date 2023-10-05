# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from holdmycomicsapi.models import Customer, User, CustomerBook, Book

class CustomerView(ViewSet):
    """HMC Customers View"""
    
    def create(self, request):
        """POST Customer"""
        
        # requests data from front end to get the data used to create the entity
        
        # retrieves User object from database
        # client data stored in request.data dictionary
        store_id = User.objects.get(pk=request.data["storeId"])
        
        # call create ORM method and pass fields as function parameters
        customer = Customer.objects.create(
            store_id = store_id,
            customer_name=request.data["customerName"],
            email=request.data["email"],
            phone=request.data["phone"],
            store_credit=request.data["storeCredit"],
        ) # customer variable is now the new customer instance, including new id
        
        # object is now serialized
        serializer = CustomerSerializer(customer)
        
        # data passed back to the front end
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # be succinct and high level in interviews, less is more
        # be focused on giving my knowledge instead of what I think question wants
        # give the answer then STOP
        # how everything connects
    
    def retrieve(self, request, pk):
        """GET Single Customer"""
        
        customer = Customer.objects.get(pk=pk) # Object Relational Mapping
        
        # Customer - name of a Django model
        # .objects - Manager instance attached to the model. It's a mechanism that Django provides to interact with the database
        # .get(pk=pk) - method provided by the manager to retrieve a single object from the database table. The pk parameter is used to specify the primary key value of the object you want to retrieve.
        
        # Customer.objects.get(pk=pk) - ORM query that instructs Django to fetch a single GameType object from the database table where the primary key matches the value provided in pk.
        
        # Django ORM allows you to interact with your database using Python code and model classes instead of writing raw SQL queries, provides a more intuitive interface, and helps you write more maintainable and portable code..
        
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def list(self, request):
        """GET All Customers"""

        customers = Customer.objects.all()
        store_id = request.query_params.get('storeId', None)
        # request method parameter holds all the information for the request from the client
        # request.query_params is a dictionary of any query parameters that were in the url
        # using .get method on a dictionary is a safe way to find if a key is present on the dictionary
        # If the 'storeId' key is not present on the dictionary it will return None
        
        if store_id is not None:
            # ORM filter method only returns customers with specific store id
            customers = customers.filter(store_id=store_id)
        serializer = CustomerSerializer(customers, many=True)
         # customers variable is now a list of Customer objects
         # many = list instead of single customer
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk):
        """PUT Customer"""
        # PUT requests expect the entire object to be sent to the server regardless of whether a field has been updated
        
        # grab customer object you want from database
        customer = Customer.objects.get(pk=pk)
        
        # setting the fields on customer to the values coming from the client
        customer.store_id = User.objects.get(pk=request.data["storeId"])
        customer.customer_name = request.data["customerName"]
        customer.email = request.data["email"]
        customer.phone = request.data["phone"]
        customer.store_credit = request.data["storeCredit"]
        
        # changes saved to data base
        customer.save()
        
        # data returned to front end
        return Response('Customer Updated', status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        """DELETE Customer"""
        # deletes a row from the database
        # retrieve, update, and destroy methods take the pk as an argument
         
        # get pk to get single object to be deleted
        customer = Customer.objects.get(pk=pk)
        
        # call delete from ORM to remove customer from database
        customer.delete()
        
        return Response('Customer Deleted', status=status.HTTP_204_NO_CONTENT)
        
    @action(methods=['get'], detail=True)
    def get_books(self, request, pk):
        """Get the books for a specific customer"""
        try:
            # Retrieve the customer books associated with the customer
            customer_books = CustomerBook.objects.filter(customer_id=pk)
            
            # Serialize the customer_books queryset using the CustomerBookWithBookSerializer
            serializer = CustomerBookWithBookSerializer(customer_books, many=True)

            return Response(serializer.data)
        except CustomerBook.DoesNotExist:
            return Response({'error': 'CustomerBook data not found'}, status=status.HTTP_404_NOT_FOUND)

        
    @action(methods=['get'], detail=False)
    def get_all_books(self, request):
        """Get all the customer books"""
        try:
            customer_books = CustomerBook.objects.all()
            serializer = CustomerBookSerializer(customer_books, many=True)
            return Response(serializer.data)
        except CustomerBook.DoesNotExist:
            return Response(False)
        
class CustomerBookSerializer(serializers.ModelSerializer):
    book_details = serializers.SerializerMethodField()

    class Meta:
        model = CustomerBook
        fields = ['customer_id', 'book_id', 'book_details']

    def get_book_details(self, obj):
        try:
            book = Book.objects.get(id=obj.book_id)
            # Serialize the book data using your BookSerializer
            book_serializer = BookSerializer(book)
            return book_serializer.data
        except Book.DoesNotExist:
            return None

# class CustomerBookSerializer(serializers.ModelSerializer):
#     """JSON Serializer for Customer Books"""
#     class Meta:
#         model = CustomerBook
#         fields = ('id', 'customer', 'book')
#         depth = 1
      
class CustomerSerializer(serializers.ModelSerializer):
    """JSON Serializer for Customers"""
  
    class Meta:
        # The Meta class hold the configuration for the serializer.
        model = Customer
        fields = ('id', 'store_id', 'customer_name', 'email', 'phone', 'store_credit')
        depth = 1
        # GET methods do not include nested data, need "depth" to get that sweet Nestle Data
        
class BookSerializer(serializers.ModelSerializer):
    """JSON Serializer for Users"""
      
    class Meta:
        model = Book
        fields = ('id', 'image_url', 'publisher', 'title', 'price', 'description', 'release_date')
        depth=1
        
class CustomerBookWithBookSerializer(serializers.ModelSerializer):
    """JSON Serializer for Customer Book Details"""
    
    book = BookSerializer()
    class Meta:
        model = CustomerBook
        fields = ('id', 'customer', 'book')
        depth = 1
        
# ORM provides a way to map between objects in your programming language and tables in a relational database
