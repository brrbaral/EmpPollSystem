from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from poll.models import *
from django.views.generic import View
from django.views.generic import ListView,DetailView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from EmpMS.decorators import admin_hr_required,admin_only
from poll.forms import PollForm, ChoiceForm

#3 VIEWS IN A SINGLE CLASS
# class PollView(View):
#     decorators = [login_required, admin_hr_required]
#
#     @method_decorator(decorators)
#     def get(self, request, id=None):
#         if id: #IF THERE IS ID THEN IT IS TO EDIT
#             question = get_object_or_404(Question, id=id)
#             poll_form = PollForm(instance=question)
#             choices = question.choice_set.all()
#             choice_forms = [ChoiceForm(prefix=str(choice.id), instance=choice) for choice in choices]
#             template = 'polls/edit_poll.html'
#         else: #IF THERE IS NO ID THEN IT IS TO ADD NEW
#             poll_form = PollForm(instance=Question())
#             choice_forms = [ChoiceForm(prefix=str(x), instance=Choice()) for x in range(3)]
#             template = 'polls/new_poll.html'
#         context = {'poll_form': poll_form, 'choice_forms': choice_forms}
#         return render(request, template, context)
#
#     @method_decorator(decorators)
#     def post(self, request, id=None): # ADD NEW POLL EG- USERfORM(REQUEST.POST) IN EVERY FORMS
#         context = {}
#         if id:
#             return self.put(request, id)
#         poll_form = PollForm(request.POST, instance=Question())
#         choice_forms = [ChoiceForm(request.POST, prefix=str(x), instance=Choice()) for x in range(0, 3)]
#         if poll_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
#             new_poll = poll_form.save(commit=False)
#             new_poll.created_by = request.user
#             new_poll.save()
#             for cf in choice_forms:
#                 new_choice = cf.save(commit=False)
#                 new_choice.question = new_poll
#                 new_choice.save()
#             return HttpResponseRedirect('/polls/')
#         context = {'poll_form': poll_form, 'choice_forms': choice_forms}
#         return render(request, 'polls/new_poll.html', context)
#
#     @method_decorator(decorators)
#     def put(self, request, id=None):
#         context = {}
#         question = get_object_or_404(Question, id=id)
#         poll_form = PollForm(request.POST, instance=question)
#         choice_forms = [ChoiceForm(request.POST, prefix=str(
#             choice.id), instance=choice) for choice in question.choice_set.all()]
#         if poll_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
#             new_poll = poll_form.save(commit=False)
#             new_poll.created_by = request.user
#             new_poll.save()
#             for cf in choice_forms:
#                 new_choice = cf.save(commit=False)
#                 new_choice.question = new_poll
#                 new_choice.save()
#             return redirect('polls_list')
#         context = {'poll_form': poll_form, 'choice_forms': choice_forms}
#         return render(request, 'polls/edit_poll.html', context)
#
#     @method_decorator(decorators)
#     def delete(self, request, id=None):
#         question = get_object_or_404(Question)
#         question.delete()
#         return redirect('polls_list')

#USING FUNCTION BASED VIEW FOR CREATE NEW POLL
@login_required(login_url='login')
@admin_hr_required
def Poll_Add(request):
    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        choice_forms = [ChoiceForm(request.POST, prefix=str(x), instance=Choice()) for x in range(0, 3)]
        if poll_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            new_poll = poll_form.save(commit=False)
            new_poll.created_by = request.user
            new_poll.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.question = new_poll
                new_choice.save()
            return HttpResponseRedirect('/polls/')
        return render(request, 'polls/new_poll.html',{'poll_form': poll_form, 'choice_forms': choice_forms} )
    else:
        poll_form = PollForm(request.POST)
        choice_forms = [ChoiceForm(request.POST, prefix=str(x), instance=Choice()) for x in range(0, 3)]
        return render(request, 'polls/new_poll.html', {'poll_form': poll_form, 'choice_forms': choice_forms})

#USING FUCNTION BASED VIEW FOR EDITING THE EXISTING POLL
@login_required(login_url='login')
@admin_hr_required
def Poll_Edit(request, id=None):
    question = get_object_or_404(Question, id=id)
    if request.method == 'POST':
        poll_form = PollForm(request.POST, instance=question)
        choice_forms = [ChoiceForm(request.POST, prefix=str(choice.id), instance=choice) for choice in question.choice_set.all()]
        if poll_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            new_poll = poll_form.save(commit=False)
            new_poll.created_by = request.user
            new_poll.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.question = new_poll
                new_choice.save()
            return HttpResponseRedirect('/polls/')
        return render(request,'polls/edit_poll.html',{'poll_form': poll_form, 'choice_forms': choice_forms})
    else:
        poll_form = PollForm(request.POST, instance=question)
        choice_forms = [ChoiceForm(request.POST, prefix=str(choice.id), instance=choice) for choice in question.choice_set.all()]
        return render(request, 'polls/edit_poll.html', {'poll_form': poll_form, 'choice_forms': choice_forms})

#USING FUNCTION BASED VIEW TO DELETE
@login_required(login_url='login')
@admin_hr_required
def Poll_Delete(request,id=None):
    question=get_object_or_404(Question,id=id)
    if request.method == 'POST':
        question.delete()
        return HttpResponseRedirect(reverse('polls_list'))
    else:
        return render(request,'polls/poll_delete.html',{'question':question})










# Create your views here.
class IndexView(ListView):
    template_name = 'polls/index.html'
    model = Question
    context_object_name = 'questions'
    #PASSING CONTEXT DICTIONARY IN CLASS BASED VIEW
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='poll'
        return context

class Details(LoginRequiredMixin,DetailView):
    template_name = 'polls/details.html'
    model = Question
    context_object_name = 'question'

@login_required(login_url='/login/')
def poll(request,id=None):
    if request.method=="GET":
        try:
            question=Question.objects.get(id=id)

        except:
            raise Http404
        context={}
        context['question']=question
        return render(request, 'polls/poll.html',context)
    if request.method=="POST":
        user_id=1
        print(request.POST)
        ret=Answer.objects.create(user_id=user_id, choice_id=request.POST['choice'])
        if ret:
            return HttpResponse("your vote has been successfully submited")
        else:
            return HttpResponse("Your vote is not submitted ")

