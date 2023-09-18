import datetime
from dateutil.relativedelta import relativedelta
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status, filters
import requests
import environ
from holdmycomicsapi.models import Book

env = environ.Env()

class SearchView(ViewSet):
    """HMC Books View"""
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    
    def list(self, request):
        """GET Books for a Specific Week"""

        # Calculate the start and end dates based on the selected week
        today = datetime.date.today()
        
        two_weeks_later = today + relativedelta(days=14)

        three_weeks_later = today + relativedelta(days=21)

        # Format the start and end dates as strings
        two_str = two_weeks_later.strftime('%Y-%m-%d')
        
        three_str = three_weeks_later.strftime('%Y-%m-%d')
        
        # Print the date strings
        print(f"Two Weeks Later: {two_str}")
        print(f"Three Weeks Later: {three_str}")

        # Build the API URL with the calculated date range
        api_url = f"https://metron.cloud/api/issue/?store_date_range_after={two_str}&store_date_range_before={three_str}"

        response = requests.get(api_url, auth=(env('METRON_USERNAME'), env('METRON_PASSWORD')), timeout=60)
        
        json = response.json()
        books = []
        
        for item in json['results']:
            book = Book(
                id=item.get('id'),
                image_url=item.get('image'),
                publisher='',
                title=item.get('issue', ''),
                price=0,
                description='',
                release_date=''
            )
            book.save()
            books.append(book)
        
        # Serialize the Book objects
        serializer = BookSerializer(books, many=True)
        
        # Return the serialized data along with the HTTP 200 OK status
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class BookSerializer(serializers.ModelSerializer):
    """JSON Serializer for Users"""
      
    class Meta:
        model = Book
        fields = ('id', 'image_url', 'publisher', 'title', 'price', 'description', 'release_date')
