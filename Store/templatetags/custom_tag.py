from django.template.defaulttags import register
from django.template.defaultfilters import stringfilter
import babel.numbers

def get_currency(amount):
    return babel.numbers.format_currency(amount, "NGN", locale='en_NG')[:-3]


@register.filter
def currency(amount):
    output=get_currency(amount)
    return output