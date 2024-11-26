import os

from rest_framework import serializers
import bcrypt
import jwt
from backend import settings
from rest_framework.request import Request
from datetime import datetime,timedelta
from .models import User


def validate_password(value):
    if not any(char.isupper() for char in value):
        raise serializers.ValidationError("Password must contain at least one uppercase letter.")
    if not any(char.islower() for char in value):
        raise serializers.ValidationError("Password must contain at least one lowercase letter.")
    if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/' for char in value):
        raise serializers.ValidationError("Password must contain at least one symbol.")
    return value

def authenticate_user_via_password(email, password):
    password = validate_password(password)
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise serializers.ValidationError("User with this email does not exist.")
    if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        return user
    raise serializers.ValidationError("Incorrect password.")

def get_token_from_request(req: Request):
    if settings.STORE_TOKEN_IN_HTTP_ONLY_COOKIE:
        return req.COOKIES.get('token')
    token = req.headers.get('Authorization')
    if not token:
        raise serializers.ValidationError("Token not provided.")
    try:
        return token.split(' ')[1]
    except IndexError:
        raise serializers.ValidationError("Token not provided.")

def decode_and_validate_token(token):
    try:
        return decode_token(token)
    except jwt.ExpiredSignatureError:
        raise serializers.ValidationError("Token expired.")
    except jwt.InvalidTokenError:
        raise serializers.ValidationError("Invalid token.")

def get_user_from_token(decoded_token):
    email = decoded_token.get('email')
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        raise serializers.ValidationError("User with this email does not exist.")

def authenticate_user_via_token(req: Request):
    token = get_token_from_request(req)
    decoded_token = decode_and_validate_token(token)
    return get_user_from_token(decoded_token)


def hash_password(value,salt=None):
    validate_password(value)
    salt = bcrypt.gensalt() if salt is None else salt.encode('utf-8')
    hashed = bcrypt.hashpw(value.encode('utf-8'), salt)
    return hashed, salt


def generate_token(email):
    secret = settings.JWT_SECRET
    algorithm = settings.JWT_ALGORITHM
    expiration = settings.JWT_EXPIRATION_DELTA
    return jwt.encode({'email': email, 'exp': datetime.now() + timedelta(seconds=expiration)}, secret, algorithm=algorithm)

def decode_token(token):
    secret = settings.JWT_SECRET
    algorithm = settings.JWT_ALGORITHM
    return jwt.decode(token, secret, algorithms=[algorithm])


def get_authenticated_user(req: Request):
    try:
        return authenticate_user_via_token(req), None
    except serializers.ValidationError as e:
        return None, e
def is_user_admin(user):
    return user.role == 'admin'

