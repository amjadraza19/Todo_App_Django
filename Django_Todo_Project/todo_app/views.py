from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.forms.models import model_to_dict
from .models import TodoList
import utl  # Assuming utl is a custom utility module where is_auth is defined
import utils as utl

from .serializers import TaskSerializer


@api_view(['POST'])
@utl.is_auth
def add_todo_task(request):
    try:
        # Getting the task title and details from the request
        title = request.data.get('title')
        details = request.data.get('details')

        if not title:
            return Response({'error': 'Title cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)

        # Assuming request.user_id is set by the @utl.is_auth decorator
        user_id = request.user_id

        # Adding the task to the Database Table -> TodoList
        temp_task = TodoList(title=title, details=details, user_id=user_id)
        temp_task.save()

        # Converting the newly added task to a dictionary format and returning it as JSON
        task_json = model_to_dict(temp_task, fields=['id', 'title', 'details', 'date', 'user_id'])

        return Response(task_json, status=status.HTTP_201_CREATED)

    except TodoList.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@utl.is_auth
def view_todo_task(request):
    try:
        # Assuming request.user_id is set by the @utl.is_auth decorator
        user_id = request.user_id

        # Retrieving the task from the database
        task = TodoList.objects.filter(user_id=user_id)

        if not task.exists():
            return Response({'error': 'Task not found '}, status=status.HTTP_404_NOT_FOUND)

         # Serialize the updated task
        task_serializer = TaskSerializer(task, many=True)

        return Response(task_serializer.data, status=status.HTTP_200_OK)

    except Exception as e:

     return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@utl.is_auth
def update_todo_task(request):
    try:
        user_id = request.user_id

        # Retrieve the specific task by user_id
        task = TodoList.objects.get(user_id=user_id)

        #updated new task
        task.title = request.data.get('title', task.title)
        task.details = request.data.get('details', task.details)
        task.date = request.data.get('date', task.date)

        # Serialize the updated task
        task_serializer = TaskSerializer(task, data=request.data, partial=True)

        if task_serializer.is_valid():
            task_serializer.save()
            return Response(task_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except TodoList.DoesNotExist:
        return Response({'error': 'Task not found or not authorized'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@utl.is_auth
def delete_todo_task(request):
    try:
        user_id = request.user_id

        task = TodoList.objects.get(user_id=user_id)

        # delete a specific task
        task.delete()

        return Response({'message': 'Task deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    except TodoList.DoesNotExist:
        return Response({'error': 'Task not found or not authorized'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
