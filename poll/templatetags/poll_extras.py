from poll.models import Question
from django import template
register=template.Library()

# 1)THIS IS FOR DJANGO TEMPLATE FILTER
def upper(value):
    return value.upper()
#THE FIRST UPPER IS THE NAME OF FILTER AND SECOND UPPER IS THE NAME OF THE FUCNTION
register.filter('upper',upper)


#2) THIS IS FOR DJANGO TEMPLATE TAGS
@register.simple_tag
def recent_polls(n=5):
    questions=Question.objects.all().order_by('-created_at')
    return questions[0:n]
    #NOW NEED TO REGISTER THIS ABOVE

