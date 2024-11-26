from functools import wraps
from rest_framework.response import Response
from rest_framework import status

from authentication.utils import get_authenticated_user


def permission_required(*levels):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(view, req, *args, **kwargs):
            current_user,e = get_authenticated_user(req)
            if current_user is None:
                return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
            if current_user.role not in levels:
                return Response({'message': 'Forbidden: You do not have the necessary permissions to access '}, status=status.HTTP_403_FORBIDDEN)
            return view_func(view, req, *args, **kwargs)
        return _wrapped_view
    return decorator