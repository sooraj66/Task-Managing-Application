from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate
from .models import Task
from .serializers import TaskSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator


# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def user_signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if User.objects.filter(Q(username=username) | Q(email=email)).exists():
        return Response({'error': 'Username or email already exist'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(username=username, email=email)  #Create new user object
    user.set_password(password)  # For hashing the password
    user.save()
    return Response({'message': "user created successfully"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tasks_list(request):

    page = request.GET.get('page', 1)

    query = request.GET.get('q', '')  # Get the search query from the URL parameters

    tasks = Task.objects.all()

    if query:
        tasks = tasks.filter(title__icontains=query)  # Search for tasks with a title containing the query

    status_filter = request.GET.get('status', None)  # Filter task by status

    if status_filter is not None:
        tasks = tasks.filter(status=status_filter)

    tasks = tasks.order_by("-updated_at")
    total_tasks = tasks.count()

    task_paginator = Paginator(tasks, 10)
    paginated_tasks = task_paginator.get_page(page)

    serializer = TaskSerializer(paginated_tasks, many=True)
    json_data = {
        'tasks': serializer.data,
        'total_tasks': total_tasks,
        'page': paginated_tasks.number,
        'total_pages': task_paginator.num_pages
    }

    return Response(json_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task(request, id):
    task = get_object_or_404(Task,pk=id)
    serializer = TaskSerializer(task, many=False)
    json_data = serializer.data
    return Response(json_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH','PUT'])
@permission_classes([IsAuthenticated])
def update_task(request, id):
    task = get_object_or_404(Task,pk=id)
    serializer = TaskSerializer(instance=task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, id):
        task = get_object_or_404(Task,pk=id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
