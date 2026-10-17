from rest_framework.permissions import BasePermission
from .models import Role

class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
   
        return  obj.author == request.user


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Role.ADMIN













