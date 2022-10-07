from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Класс, формирующий админ-панель сайта, раздел: пользователи."""
    list_display = (
        'username', 'email', 'first_name',
        'last_name', 'role', 'bio', 'confirmation_code',
    )
    search_fields = ('username', 'role',)
    list_filter = ('username',)
    empty_value_display = 'пустое поле'
