import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
import requests
import environ
from holdmycomicsapi.models import Book, Customer, CustomerBook

env = environ.Env()

class BookView(ViewSet):
    """HMC Books View"""
    
    def retrieve(self, request, pk):
        """GET Single Book"""
        
        api_url = f"https://metron.cloud/api/issue/{pk}"
        response = requests.get(api_url, auth=(env('METRON_USERNAME'), env('METRON_PASSWORD')), timeout=60)
        
        if response.status_code == 200:
            # Deserialize the JSON data
            json_data = response.json()
            
            # Extract relevant fields from the JSON data
            book_id = json_data.get('id')
            image_url = json_data.get('image', '')
            price = json_data.get('price', 0)
            description = json_data.get('desc', '')
            
            # Extract and set the publisher information
            publisher_data = json_data.get('publisher')
            publisher_name = publisher_data.get('name') if publisher_data else ''
            
            # Extract and set the title information
            title_data = json_data.get('series')
            title_name = title_data.get('name') if title_data else ''
            number = json_data.get('number', '')
            title_name = f"{title_name} #{number}"

            # Create a Book instance using the extracted fields
            book = Book(
                id=book_id,
                image_url=image_url,
                publisher=publisher_name,
                title=title_name,
                price=price,
                description=description
            )
            
            # Serialize the Book object
            serializer = BookSerializer(book)
            
            # Return the serialized data along with the HTTP 200 OK status
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif response.status_code == 404:
            # Handle the case where the book with the specified ID is not found
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Handle other error cases
            return Response({'error': 'Failed to fetch data from external API'}, status=response.status_code)
    
    def list(self, request):
        """GET Books Released Between Monday and Sunday of the Current Week"""
        
        # Calculate the start date (Monday) of the current week
        today = datetime.date.today()
        current_day_of_week = today.weekday()  # 0 = Monday, 1 = Tuesday, ..., 6 = Sunday
        
        # Calculate the number of days to subtract to reach the start of the current week (0 days for Monday, 1 day for Tuesday, etc.)
        days_until_monday = current_day_of_week
        start_of_week = today - datetime.timedelta(days=days_until_monday)
    
        # Calculate the end date (Sunday) of the current week
        end_of_week = start_of_week + datetime.timedelta(days=6)  # 6 days from Monday to Sunday
    
        # Format the start and end dates as strings (e.g., "2023-09-04" for Monday and "2023-09-10" for Sunday)
        start_date_str = start_of_week.strftime('%Y-%m-%d')
        end_date_str = end_of_week.strftime('%Y-%m-%d')
        
         # Build the API URL with the calculated date range
        api_url = f"https://metron.cloud/api/issue/?store_date_range_after={start_date_str}&store_date_range_before={end_date_str}"

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
                description=''
            )
            book.save()
            books.append(book)
        
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
        
        # Delete the CustomerBook instance            
        customer_book.delete()
        
        # Return a success response
        return Response({'message': 'Book removed from Customer'}, status=status.HTTP_204_NO_CONTENT)
    
    # Defines a custom action named removefromcustomer within a viewset. The action is triggered by a DELETE request and removes a specific book from a specific customer. It retrieves the customer and book instances based on the provided data, then gets the specific CustomerBook instance connecting the customer and book. It then deletes this relationship.

class BookSerializer(serializers.ModelSerializer):
    """JSON Serializer for Users"""
      
    class Meta:
        model = Book
        fields = ('id', 'image_url', 'publisher', 'title', 'price', 'description')
