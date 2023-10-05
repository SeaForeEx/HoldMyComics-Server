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
    
    def create(self, request):
        """POST Book"""
        
        # requests data from front end to get the data used to create the entity
        
        # call create ORM method and pass fields as function parameters
        book = Book.objects.create(
            image_url=request.data["imageUrl"],
            publisher=request.data["publisher"],
            title=request.data["title"],
            price=request.data["price"],
            description=request.data["description"],
            release_date=request.data["releaseDate"],
        ) # customer variable is now the new customer instance, including new id
        
        # object is now serialized
        serializer = BookSerializer(book)
        
        # data passed back to the front end
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk):
        """GET Single Book"""
        
        api_url = f"https://metron.cloud/api/issue/{pk}/"
        print(api_url)
        response = requests.get(api_url, auth=(env('METRON_USERNAME'), env('METRON_PASSWORD')), timeout=60)
        
        print(response.status_code)
        
        if response.status_code == 200:
            # Deserialize the JSON data
            print(response.content)
            json_data = response.json()
            
            # Add print statements to check data retrieval
            print("Retrieved JSON data:", json_data)
            
            # Extract relevant fields from the JSON data
            book_id = json_data.get('id')
            image_url = json_data.get('image', '')
            price = json_data.get('price', '')
            description = json_data.get('desc', '')
            release_date = json_data.get('store_date', '')
            
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
                description=description,
                release_date=release_date
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
        """GET Books for a Specific Week"""
        # Get the selected week from the query parameters (formatted date from the frontend)
        selected_date = request.GET.get('formattedDate')  # matches 'date' to 'formattedDate' on frontend

        # Convert the selected_date (formatted date) to a datetime object
        selected_date = datetime.datetime.strptime(selected_date, '%Y-%m-%d').date()

        # Calculate the start and end dates based on the selected week
        today = datetime.date.today()
        if selected_date == today:
            # Calculate the start date for this week
            start_of_week = today - datetime.timedelta(days=today.weekday())
        else:
            # Calculate the start date for the selected week
            start_of_week = selected_date - datetime.timedelta(days=selected_date.weekday())

        end_of_week = start_of_week + datetime.timedelta(days=6)

        # Format the start and end dates as strings
        start_date_str = start_of_week.strftime('%Y-%m-%d')
        end_date_str = end_of_week.strftime('%Y-%m-%d')

        # Build the API URL with the calculated date range
        api_url = f"https://metron.cloud/api/issue/?store_date_range_after={start_date_str}&store_date_range_before={end_date_str}"

        response = requests.get(api_url, auth=(env('METRON_USERNAME'), env('METRON_PASSWORD')), timeout=60)
        
        json = response.json()
        books = []
        
        for item in json['results']:
            rating = item.get("rating", {}).get("name")
            print(f'{rating}')
            book = Book(
                id=item.get('id'),
                image_url=item.get('image'),
                publisher='',
                title=item.get('issue', ''),
                price='',
                description='',
                release_date=''
            )
            book.save()
            books.append(book)
        
        # Serialize the Book objects
        serializer = BookSerializer(books, many=True)
        
        # Return the serialized data along with the HTTP 200 OK status
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk):
        """PUT Book"""
        # PUT requests expect the entire object to be sent to the server regardless of whether a field has been updated
        
        # grab book object you want from database
        book = Book.objects.get(pk=pk)
        
        # setting the fields on customer to the values coming from the client
        
        book.image_url = request.data["imageUrl"]
        book.publisher = request.data["publisher"]
        book.title = request.data["title"]
        book.price = request.data["price"]
        book.description = request.data["description"]
        book.release_date = request.data["releaseDate"]
        
        # changes saved to data base
        book.save()
        
        # data returned to front end
        return Response('Customer Updated', status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['GET'])
    def booksthisweek(self, request):
        """Books Released This Week"""

        # Calculate the start and end dates based on the selected week
        today = datetime.date.today()
       
        # Calculate the start date for this week
        start_of_week = today - datetime.timedelta(days=today.weekday())
        
        end_of_week = start_of_week + datetime.timedelta(days=6)

        # Format the start and end dates as strings
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
                price=item.get('price', ''),
                description='',
                release_date=''
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
        fields = ('id', 'image_url', 'publisher', 'title', 'price', 'description', 'release_date')
        
class CustomerBookWithBookSerializer(serializers.ModelSerializer):
    """JSON Serializer for Customer Book Details"""
    
    book = BookSerializer()
    class Meta:
        model = CustomerBook
        fields = ('id', 'customer', 'book')
        depth = 2
