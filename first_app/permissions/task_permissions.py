from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешает редактирование объектов только их владельцам, остальным - только чтение.
    """

    def has_object_permission(self, request, view, obj):
        # Все пользователи могут просматривать
        if request.method in SAFE_METHODS: # тоже самое что in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Только владелец может изменять объект
        return obj.owner == request.user
