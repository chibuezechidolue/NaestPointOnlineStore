from django.template.defaulttags import register
from django.template.defaultfilters import stringfilter
import babel.numbers

def get_currency(amount):
    return babel.numbers.format_currency(amount, "NGN", locale='en_NG')[:-3]


@register.filter
def currency(amount):
    output=get_currency(amount)
    return output


# from django import template
# register = template.Library()

@register.filter
def index(list, i):
    return list[i]






from itertools import islice 

@register.filter
def split_dict(dictionary,i):
    inc = iter(dictionary.items()) 
    res1 = dict(islice(inc, len(dictionary) // 2)).items() 
    res2 = dict(inc).items() 
    if i==0:
        return res1
    else:
        return res2
    