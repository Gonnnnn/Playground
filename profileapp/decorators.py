from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from .models import *

def account_ownership_required(func):

    def decorated(request, *args, **kwargs):
        profile = Profile.objects.get(pk=kwargs['pk'])
        if not request.user == profile.user:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)

    return decorated