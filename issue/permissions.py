from rest_framework import permissions
from issue.mappers import AssignedToRoleMappers

class AssigneePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
 
    def has_object_permission(self, request, view, obj):
        user = request.user
        ticket = obj if obj else None
        if user.is_superuser:
            return True
        if user.role == 'Normal User':
            return True
        if ticket:
            assigned_to = ticket.assigned_to
            role1 = AssignedToRoleMappers.get(assigned_to)
            role = user.role 
            if role == role1:
                return True
        return False
    
