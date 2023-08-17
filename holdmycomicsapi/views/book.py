# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from holdmycomicsapi.models import Book

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

class BookSerializer(serializers.ModelSerializer):
    """JSON Serializer for Users"""
      
    class Meta:
        model = Book
        fields = ('id', 'image_url', 'publisher', 'title', 'price', 'description')
