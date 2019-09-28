from .models import Question
from django.contrib.auth.models import User
def polls_count(request):
    count=Question.objects.count()
    return {'polls_count':count}

def users_count(request):
    empcount=User.objects.count()
    return {'users_count':empcount}