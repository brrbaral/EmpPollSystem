from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
# Create your models here.

#CREATING ABSTRACT MODEL
class ObjectTracking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True #THIS MEANS THIS MODEL IS NOT FOR CREATING TABLE
        #IT IS FOR INHERITING THE MODEL BY SUBMODEL
        #YOU CAN ALSO ADD HERE META FIELDS WHICH WILL BE INHERITED BY SUB CLASSES
        ordering=['-created_at']#THIS WILL BE USED BY OTHERS BASE CALSSES

# class Comment(models.Model):
#     text=models.TextField(null=False, blank=False)
#     content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
#     object_id=models.PositiveIntegerField()



class Tag(ObjectTracking):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering=[] #THIS IS FOR NULLIFYING



class Question(ObjectTracking):
    title=models.TextField(null=True,blank=True)
    status=models.CharField(default='inactive',max_length=10)
    #IF THERE ARE MULTPILE HR THEN WHO CREATED THIS
    created_by=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)#BEACUSE ONE USER CAN CREATE MORE THAN ONE QUESTIONS
    start_date=models.DateTimeField(null=True,blank=True)
    end_date=models.DateTimeField(null=True,blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property   #CHOICE IS THE PROPERTY OF MODEL QUESTION
    def choices(self):
        return self.choice_set.all()

class Choice(models.Model):
    question=models.ForeignKey('poll.Question',on_delete=models.CASCADE)#ONE QUESTION HAVE MORE THAN ONE CHOICES
    text=models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    @property   #VOTES IS THE PROPERTY OF MODEL CHOICE
    def votes(self):
        return self.answer_set.count()

class Answer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    choice=models.ForeignKey(Choice,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name + '-' + self.choice.text
