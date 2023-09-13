from rest_framework.permissions import BasePermission

class IsSeller(BasePermission):
    edit_methods = ("PUT", "GET", "POST", "DELETE")

    def has_object_permission(self, request, view, obj):
        if request.user.is_seller:
            return True

        return False
    
class IsBuyer(BasePermission):
    edit_methods = ("PUT", "GET", "POST", "DELETE")

    def has_object_permission(self, request, view, obj):
        if request.user.is_buyer:
            return True

        return False