# tickets/templatetags/bulletify.py
from django import template
from django.utils.html import escape, mark_safe

register = template.Library()

@register.filter(name='bulletify')
def bulletify(value):
    if not value:
        return ''
    lines = [line.strip() for line in value.splitlines() if line.strip()]
    lis   = ''.join(f'<li>{escape(line)}</li>' for line in lines)
    return mark_safe(f'<ul>{lis}</ul>')
