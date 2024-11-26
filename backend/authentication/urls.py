from django.urls import path,include
from rest_framework.routers import SimpleRouter

from .views import *


auth_router = SimpleRouter(trailing_slash=False)
auth_router.register(prefix='users',viewset=UserView,basename='user')

urlpatterns = [
    path('',include((auth_router.urls,'Auth API'),'auth-api')),
    path('login',login,name='login'),
    path('logout',logout,name='logout'),
    path('change-password',change_password,name='change-password'),
    path('login-status',login_status,name='login-status'),
]
