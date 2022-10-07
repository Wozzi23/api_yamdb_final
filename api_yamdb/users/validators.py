from django.core.exceptions import ValidationError


def validate_username(value):
    """Проверка корректности никнейма"""
    if value == 'me':
        raise ValidationError(
            ('В имени пользователя не должно использоваться "me".'),
            params={'value': value},
        )
