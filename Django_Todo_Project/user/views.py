from urllib import request   #Importing the request module from urllib, although it is not used here
from django.contrib.auth import authenticate
from django.db.models import Q  #Importing Q object for complex queries involving OR, AND, NOT conditions
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import TodoUser
from django.utils.decorators import method_decorator

import utils as utl  # Importing a custom utility module named 'utils' and aliasing it as 'utl'

@api_view(['POST'])
def register_user(request):

    # Create an instance of UserSerializer with the incoming request data
    serializer = UserSerializer(data=request.data)

    # Check if the provided data is valid according to the serializer's
    if serializer.is_valid():

        # Save the new user to the database if the data is valid
        serializer.save()

        # Return a response with the serialized data of the newly created user
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):

    # Retrieve the username or email and password from the request data
    username_or_email = request.data.get('username')
    password = request.data.get('password')

    # Check if both username/email and password are provided
    if not username_or_email or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = None
    try:
        # Attempt to retrieve the user based on username or email
        user = TodoUser.objects.get(
            Q(username=username_or_email) | Q(email=username_or_email)
        )
    except TodoUser.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    if not(user.check_password(password)):
        return Response({'error': 'Incorrect Password'}, status=status.HTTP_400_BAD_REQUEST)

    # If the user exists and the password is correct, generate an access token
    if user:

        # Generate an access token for the authenticated user
        access_token = utl.generate_access_token(user)

        user.is_login = True  # Set login is True
        user.is_active = True  # Setting user is active or not
        user.token = str(access_token)       # Set the user's token to the string representation of the access token
        user.save()      # Save the updated user instance to the database
        user_data=UserSerializer(user).data     # Serialize the updated user instance into a dictionary format for response
        return Response({'data': {'token': access_token, **user_data}}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@utl.is_auth
def user_logout(request):
    try:

        # Retrieve the authenticated user's ID from the request object
        user_id = request.user_id

        # Fetch the user instance from the database using the user_id
        user_inst = TodoUser.objects.get(id=user_id)

        # Set the user's token to None to effectively log them out
        user_inst.token = None

        # Save the updated user instance to the database
        user_inst.save()

        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

    except TodoUser.DoesNotExist:
        # Handle the case where the user does not exist in the database
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        # Handle any other exceptions that might occur during the process
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

