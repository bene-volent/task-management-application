from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import api_view,action

from authentication.serializer.users import UserSerializer
from backend import settings
from .decorators import permission_required
from .models import User
from .serializers import UserCreateSerializer, UserPublic
from .utils import authenticate_user_via_password, hash_password, generate_token, authenticate_user_via_token, \
    get_authenticated_user


class UserView(viewsets.ViewSet):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @permission_required('admin')
    def list(self, req: Request):
        queryset = User.objects.all()
        serializer = UserPublic(queryset, many=True)
        return Response({'users': serializer.data})
        
    def create(self, req: Request):
        serializer = UserCreateSerializer(data=req.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'user': UserPublic(user).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @permission_required('admin')
    def retrieve(self, req: Request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserPublic(user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)

    @permission_required('admin')
    def update(self, req: Request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserCreateSerializer(user, data=req.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'user': UserPublic(user).data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @permission_required('admin')
    def destroy(self, req: Request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @permission_required('admin')
    def partial_update(self, req: Request, pk=None):
        
        if get_authenticated_user(req) is None:
            return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserCreateSerializer(user, data=req.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()            
            
            return Response({'user': UserPublic(user).data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get', 'put','patch','delete'], detail=False,url_path='me')
    def me(self, req: Request):
        me,e = get_authenticated_user(req)

        if me is None:
            return Response({'message': e}, status=status.HTTP_401_UNAUTHORIZED)

        if req.method == 'GET':
            return Response({'user': UserPublic(me).data}, status=status.HTTP_200_OK)

        if req.method == 'PATCH':
            serializer = UserCreateSerializer(me, data=req.data, partial=True)
            if serializer.is_valid():
                user = serializer.save()
                return Response({'user': UserPublic(user).data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if req.method == 'PUT':
            serializer = UserCreateSerializer(me, data=req.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response({'user': UserPublic(user).data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if req.method == 'DELETE':
            me.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['POST'])
def login(req: Request):
    email = req.data.get('email')
    password = req.data.get('password')
    try:
        user = authenticate_user_via_password(email, password)
    except serializers.ValidationError as e:
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError as e:
        return Response({'message': 'Invalid password format'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    store_token_in_cookie = settings.STORE_TOKEN_IN_HTTP_ONLY_COOKIE
    if store_token_in_cookie:
        res = Response({'user': UserPublic(user).data}, status=status.HTTP_200_OK)
        res.set_cookie('token', generate_token(user.email), httponly=True)
        
        return res

    return Response({'user': UserPublic(user).data,'token':generate_token(user.email)}, status=status.HTTP_200_OK)

@api_view(['POST'])
def logout(req: Request):
    store_token_in_cookie = settings.STORE_TOKEN_IN_HTTP_ONLY_COOKIE
    res = Response(status=status.HTTP_200_OK)
    if store_token_in_cookie:
        res.delete_cookie('token')
    return res

@api_view(['GET'])
def login_status(req: Request):
        me = get_authenticated_user(req)
        if me is None:
            return Response({'status':False} , status=status.HTTP_401_UNAUTHORIZED)
        return Response({'status': True}, status=status.HTTP_200_OK)

@api_view(['POST'])
def change_password(req: Request):
    user = authenticate_user_via_password(req.data.get('email'), req.data.get('current-password'))

    if user is None:
        return Response({'message': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

    hashed, salt = hash_password(req.data.get('new-password'))
    user.hashed_password = hashed
    user.salt = salt
    user.save()

    return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)





