import re

from django.core.exceptions import ValidationError
from django.utils import timezone


def username_validator(value):
    if value == 'me':
        raise ValidationError(
            'Использовать имя "me" в качестве username запрещено.'
        )

    if re.search(r'^[\w.@+-]+\Z', value) is None:
        raise ValidationError(
            'Имя может содержать буквы, цифры и символы @/./+/-/_'
        )
    return value


def year_validator(value):
    now = timezone.now().year
    if value > now:
        raise ValidationError(
            f'Дата произведения {value} не должна быть больше {now}.'
        )
    return value
