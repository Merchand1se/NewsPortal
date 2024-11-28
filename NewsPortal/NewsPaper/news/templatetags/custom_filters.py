from django import template

register = template.Library()

forbidden_words = ()

@register.filter
def hide_forbidden(value):
    words = value.split()
    result = []
    for word in words:
        if word in forbidden_words:
            result.append(word[0] + "*"*(len(word)-2) + word[-1])
        else:
            result.append(word)
    return " ".join(result)

#test Middleware
class FullMobileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)
        if request.mobile:
            prefix = 'mobile/'
        else:
            request = 'full/'
        response.template_name = prefix + response.template_name
        return response
