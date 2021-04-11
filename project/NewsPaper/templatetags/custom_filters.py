from pathlib import Path
from django import template
import os


register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    if isinstance(value, str) and isinstance(arg, int):
        return str(value) * arg
    else:
        raise ValueError(f'Нельзя умножить {type(value)} на {type(arg)}')


#  Фильтр мата

list_location = Path(__file__).absolute().parent / 'censor_list.txt'
censor_list = list_location.open().read().split(', ')[:-2]

@register.filter(name='censor')
def censor(value):
    global censor_list

    if isinstance(value, str):

        value_c = str(value)
        for i in censor_list:
            if i in value_c.split():
                value_c = value_c.replace(i, 'censored')
            else:
                pass

        return value_c
    else:
        raise ValueError(f'Нельзя применить фильтр для типа {type(value)}')