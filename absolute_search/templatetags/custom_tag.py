from django import template
from datetime import datetime

register = template.Library()

@register.filter
def index(indexable, i):
   return indexable[i]

@register.filter
def timeformat(time):
   datetime_object = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
   return datetime_object.strftime("%b %d, %Y ")