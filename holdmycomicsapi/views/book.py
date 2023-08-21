# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from holdmycomicsapi.models import Book, Customer, CustomerBook

class BookView(ViewSet):
    """HMC Books View"""
    
    def retrieve(self, request, pk):
        """GET Single Book"""
        
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book)
            return Response(serializer.data)
        except Book.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
          
    def list(self, request):
        """GET All Books"""
        
        # Retrieve all Book objects
        books = Book.objects.all()
        # Serialize the Book objects
        serializer = BookSerializer(books, many=True)
        # Return the serialized data along with the HTTP 200 OK status
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Custom action that adds a book to a customer
    @action(methods=['post'], detail=True)
    def addtocustomer(self, request, pk):
        """Add Book To Customer"""
        # Get the Customer instance using the customerId from the request data
        customer = Customer.objects.get(pk=request.data["customerId"])
        # Get the Book instance using the primary key (pk) parameter
        book = Book.objects.get(pk=pk)
            
        # Create a CustomerBook instance linking the customer and book
        CustomerBook.objects.create(
            customer=customer,
            book=book
        )
        return Response({'message': 'Book added to Customer'}, status=status.HTTP_201_CREATED)
    
    # Defines a custom action named addtocustomer within a viewset. The action is triggered by a POST request and adds a specific book to a specific customer. It first retrieves the customer and book instances based on the provided data, then creates a CustomerBook relationship between them.
    
    # Custom action that removes a book from a customer
    @action(methods=['delete'], detail=True)
    def removefromcustomer(self, request, pk):
        """Remove Book From Customer"""
        # Get the Customer instance using the customerId from the request data
        customer = Customer.objects.get(pk=request.data["customerId"])
        # Get the Book instance using the primary key (pk) parameter
        book = Book.objects.get(pk=pk)
            
        # Get the specific CustomerBook instance connecting the customer and book
        customer_book = CustomerBook.objects.get(
            customer_id=customer.id,
            book_id=book.id
        )
            
        # Delete the CustomerBook instance            customer_book.delete()
            
        # Return a success response
        return Response({'message': 'Book removed from Customer'}, status=status.HTTP_204_NO_CONTENT)
    
    # Defines a custom action named removefromcustomer within a viewset. The action is triggered by a DELETE request and removes a specific book from a specific customer. It retrieves the customer and book instances based on the provided data, then gets the specific CustomerBook instance connecting the customer and book. It then deletes this relationship.

class BookSerializer(serializers.ModelSerializer):
    """JSON Serializer for Users"""
      
    class Meta:
        model = Book
        fields = ('id', 'image_url', 'publisher', 'title', 'price', 'description')
