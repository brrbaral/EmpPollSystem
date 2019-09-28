from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic import DetailView
from django.contrib.auth.models import User
from . forms import UserForm
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# Create your views here.

class EmployeeList(LoginRequiredMixin,ListView):
    template_name = 'employee/index.html'
    model = User
    context_object_name = 'employees'


class EmployeeDetail(LoginRequiredMixin,DetailView):
    template_name = 'employee/details.html'
    model = User
    context_object_name = 'employee'

@login_required(login_url='/login')
def employee_add(request):
    if request.method=='POST':
        user_form=UserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('employee_list')#HttpResponseRedirect(reverse('employee_list'))
        else:
            return render(request,'employee/add.html',{'user_form':user_form})

    else:
        user_form=UserForm()
        return render(request,'employee/add.html',{'user_form':user_form})

@login_required(login_url='/login')
def Employee_edit(request, id=None):
    user=get_object_or_404(User, id=id)
    if request.method=='POST':
        user_form=UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            return redirect('employee_list')
        else:
            return render(request,'employee/edit.html',{'user_form':user_form})
    else:
        user_form=UserForm(instance=user)
        return render(request,'employee/edit.html',{'user_form':user_form})
class Employee_delete(LoginRequiredMixin,DeleteView):
    model = User
    template_name = 'employee/delete.html'
    success_url = '/employee'

class ProfileUpdate(UpdateView):
    fields = ['designation','salary','picture']
    template_name = 'employee/profile_update.html'
    success_url = reverse_lazy('my_profile')

    def get_object(self):
        return self.request.user.profile

class MyProfile(DetailView):
    template_name = 'employee/profile.html'

    def get_object(self):
        return self.request.user.profile