from django.urls import path,include
from rest_framework.routers import SimpleRouter

from .views import *


task_router = SimpleRouter(trailing_slash=False)
task_router.register(prefix='',viewset=TaskView,basename='task')

urlpatterns = [
    path('',include((task_router.urls,'Task API'),'task-api')),
]

