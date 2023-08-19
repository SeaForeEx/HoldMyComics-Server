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
    
    @action(methods=['post'], detail=True)
    def addtocustomer(self, request, pk):
        """Add Book To Customer"""
        customer = Customer.objects.get(pk=request.data["customerId"])
        book = Book.objects.get(pk=pk)
        added = CustomerBook.objects.create(
            customer=customer,
            book=book
        )
        return Response({'message': 'Book added to Customer'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['delete'], detail=True)
    def removefromcustomer(self, request, pk):
        """Remove Book From Customer"""
        customer = Customer.objects.get(pk=request.data["customerId"])
        book = Book.objects.get(pk=pk)
        customer_book = CustomerBook.objects.get(
            customer_id=customer.id,
            book_id=book.id
        )
        customer_book.delete()
        return Response({'message': 'Book removed from Customer'}, status=status.HTTP_204_NO_CONTENT)

class BookSerializer(serializers.ModelSerializer):
    """JSON Serializer for Users"""
      
    class Meta:
        model = Book
        fields = ('id', 'image_url', 'publisher', 'title', 'price', 'description')
