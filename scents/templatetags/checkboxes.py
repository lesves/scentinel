from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="checkbox", is_safe=True)
def checkbox(value):
	return mark_safe(f"<input type=\"checkbox\" {"checked" if value else ""} disabled />")
