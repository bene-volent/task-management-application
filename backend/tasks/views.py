from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from authentication.utils import get_authenticated_user
from .models import Task
from .serializers import TaskSerializer


class TaskView(ViewSet):
    def authenticate_user(self, req: Request):
        user, e = get_authenticated_user(req)
        if user is None:
            return None, Response({'message': e}, status=status.HTTP_401_UNAUTHORIZED)
        return user, None

    def list(self, req: Request):

        user,e = self.authenticate_user(req)

        if user.role == 'admin':
            queryset = Task.objects.all()
        else:
            queryset = Task.objects.filter(user_id=user.id)

        serializer = TaskSerializer(queryset, many=True)
        return Response({'length':len(serializer.data),'tasks': serializer.data})
    
    def create(self, req: Request):
        user, e = self.authenticate_user(req)

        req.data['user'] = user.id
        serializer = TaskSerializer(data=req.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response({'task': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, req: Request, pk=None):
        user, e = self.authenticate_user(req)

        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'message': 'Task does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if user.role != 'admin' and task.user != user:
            return Response({'message': 'You are not authorized to view this task'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = TaskSerializer(task)
        return Response({'task': serializer.data}, status=status.HTTP_200_OK)

    def partial_update(self, req: Request, pk=None):
        user, e = self.authenticate_user(req)

        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'message': 'Task does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if user.role != 'admin' and task.user != user:
            return Response({'message': 'You are not authorized to update this task'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = TaskSerializer(task, data=req.data, partial=True)
        if serializer.is_valid():
            task = serializer.save()
            return Response({'task': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, req: Request, pk=None):
        user,e = get_authenticated_user(req)

        if user is None:
            return Response({'message': e}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'message': 'Task does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if user.role != 'admin' and task.user != user:
            return Response({'message': 'You are not authorized to delete this task'}, status=status.HTTP_401_UNAUTHORIZED)

        task.delete()
        return Response({'message':"Task deleted successfully" },status=status.HTTP_204_NO_CONTENT)