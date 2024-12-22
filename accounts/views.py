from django.views.generic import CreateView, View
from django.contrib.auth.models import User
from .forms import CustomSignupForm

class SignUp(CreateView):
    model = User
    form_class = CustomSignupForm
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'

class Logout(View):
    model = User
    success_url = 'signup/'
    template_name = 'registration/Logout.html'

