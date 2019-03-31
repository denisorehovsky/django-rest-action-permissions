from rest_framework.permissions import (
    AllowAny, BasePermission, IsAdminUser, IsAuthenticated
)
from rest_action_permissions.permissions import ActionPermission


class IsTweetOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class TweetPermission(ActionPermission):
    enough_perms = IsAdminUser

    create_perms = IsAuthenticated
    retrieve_perms = AllowAny
    list_perms = AllowAny
    update_perms = IsTweetOwner
    delete_perms = IsTweetOwner
    retweet_perms = IsAuthenticated
    undo_retweet_perms = IsAuthenticated

    read_perms = AllowAny
    write_perms = IsAuthenticated & IsTweetOwner
