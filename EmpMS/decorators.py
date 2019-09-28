from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied

def admin_hr_required(view_func):
    def wrap(request, *args, **kwargs): #WHATEVER TAKEN BY THIS FUNCTION WILL BE TAKEN BY OUR VIEW FUNCTION
        allowed_roles=["Admin", "HR"]
        if request.role in allowed_roles:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('employee_list'))
    return wrap

def admin_only(view_func):
    def wrap(request, *args, **kwargs):
        if request.role == "Admin":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('employee_list'))
    return wrap