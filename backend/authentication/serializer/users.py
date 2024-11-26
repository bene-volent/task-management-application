
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from ..model.users import User

from ..utils import hash_password


class UserCreateSerializer(ModelSerializer):
    password = serializers.CharField(min_length=5, max_length=16)
    photo = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = User
        fields = ['fname', 'lname', 'email', 'password', 'photo','bio','role','is_verified']

    def create(self, validated_data):
        hashed,salt = hash_password(validated_data['password'])
        hashed = hashed.decode('utf-8')
        salt = salt.decode('utf-8')

        user = User(
            fname=validated_data['fname'],
            lname=validated_data['lname'],
            email=validated_data['email'],
            hashed_password=hashed,
            photo=validated_data.get('photo'),
            bio=validated_data.get('bio', ''),
            role=validated_data.get('role', 'user'),
            is_verified=validated_data.get('is_verified'),
            salt = salt
        )
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            hashed,salt = hash_password(validated_data['password'])
            hashed = hashed.decode('utf-8')
            salt = salt.decode('utf-8')
            instance.hashed_password = hashed
            instance.salt = salt

        return super().update(instance, validated_data)
        
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserPublic(ModelSerializer):
    class Meta:
        model = User
        exclude = ['hashed_password','salt']
        




    
        
        
