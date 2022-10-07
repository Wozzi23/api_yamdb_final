from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    """
    Собственный метод проверки доступа к модели.
    Доступ к модели есть только у аминистрации.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_admin
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_admin
            or request.user.is_staff
        )


class IsAdminOrAuthorOnly(permissions.BasePermission):
    """
    Собственный метод проверки доступа к модели
    безопасные методы доступны всем пользователям,
    остальные только администрации или автору.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )


class AdminOrReadOnly(permissions.BasePermission):
    """
    Собственный метод проверки доступа к модели
    безопасные методы доступны всем пользователям,
    остальные только администрации
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.is_authenticated:
                return request.user.is_admin
