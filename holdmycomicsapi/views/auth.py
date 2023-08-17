from holdmycomicsapi.models import User  # Importing the User model from mvcapi.models
from rest_framework.decorators import api_view  # Importing the api_view decorator from rest_framework.decorators
from rest_framework.response import Response  # Importing the Response class from rest_framework.response

@api_view(['POST'])
def check_user(request):
    """
    Checks to see if User has associated User.
    """  
    uid = request.data['uid']  # Extract the 'uid' parameter from the request data   
    # Query the User model to find the user with the given UID
    user = User.objects.filter(uid=uid).first()   
    if user is not None:
        # If the user exists, create a dictionary containing the user's information
        data = {
            'id': user.id,
            'user_name': user.user_name,
            'store_name': user.store_name,
            'email': user.email,
            'uid': user.uid
        }
        return Response(data)  # Return the user's information in the response
    else:
        data = {'valid': False}  # If the user does not exist, create a dictionary indicating that the user is not valid
        return Response(data)  # Return the validation response

@api_view(['POST'])
def register_user(request):
    """
    Handles the creation of a new gamer for authentication.
    
    This function is a view that handles the HTTP POST request. It creates a new User record in the database using the provided
    user information and returns the created user's information.
    
    Args:
        request: The HTTP request object containing the data sent by the client.
            - The following parameters are expected to be present in the request data:
                - 'user_name': The username of the new user.
                - 'email': The email of the new user.
                - 'profile_image_url': The profile image URL of the new user.
                - 'bio': The bio of the new user.
                - 'uid': The UID of the new user.
    
    Returns:
        A Response object containing the created user's information.
    """
    
    # Create a new User record in the database using the provided user information
    user = User.objects.create(
        user_name=request.data['user_name'],
        store_name=request.data['store_name'],
        email=request.data['email'],
        uid=request.data['uid']
    )

    # Create a dictionary containing the created user's information
    data = {
        'id': user.id,
        'user_name': user.user_name,
        'store_name': user.store_name,
        'email': user.email,
        'uid': user.uid
    }
    
    return Response(data)  # Return the created user's information in the response
