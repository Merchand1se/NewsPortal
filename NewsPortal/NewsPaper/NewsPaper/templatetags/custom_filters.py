from better_profanity import profanity
from django import template

register = template.Library()



@register.filter()
def censor(value):
    censored = profanity.censor(value, "*")
    return censored
