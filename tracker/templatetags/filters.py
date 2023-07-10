from datetime import datetime, timedelta

from django import template


register = template.Library()


@register.filter
def get_month(date):
    print('#' * 50)
    print(date)
    month = datetime.strptime(date, '%d.%m.%Y')
    print(month)
    return month.strftime('%B')
