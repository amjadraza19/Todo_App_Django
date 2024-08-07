from django.urls import path
from .views import add_todo_task, view_todo_task, update_todo_task, delete_todo_task

urlpatterns = [
    path('new-task/', add_todo_task, name='todo_task'),
    path('view-task/', view_todo_task, name='view_task'),
    path('update-task/', update_todo_task, name='update_task'),
    path('delete-task/', delete_todo_task, name='delete_task'),
]