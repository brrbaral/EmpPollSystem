from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User,Group
from employee.models import Profile

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    role=forms.ModelChoiceField(queryset=Group.objects.all())

    class Meta:
        model=User
        fields=['first_name','last_name','email','username','password']

        label={
            'password':'Password'
        }

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            #WE GET THE 'INITIAL' KEYWORD ARGUMENT OR INITIALIZE IT
            #AS A DICT IF IT DIDN'T EXIST
            initial=kwargs.setdefault('initial',{})
            #THE WIDGET FOR A ModelMultipleChoiceField expects
            #A LIST OF PRIMARY KEY FOR THE SELECTED DATA
            if kwargs['instance'].groups.all():
                initial['role']=kwargs['instance'].groups.all()[0]
            else:
                initial['role']=None
        forms.ModelForm.__init__(self, *args, **kwargs)

    def clean_email(self):
        if self.cleaned_data['email'].endswith('.com'):
            return self.cleaned_data['email']
        else:
            raise ValidationError("Email id is not valid")

    def save(self):
        password=self.cleaned_data.pop('password')#JUST REMOVED PASSWORD FROM CLEANED_DATA DICTIONARY
        role=self.cleaned_data.pop('role')
        u=super().save()
        u.groups.set([role])
        u.set_password(password)
        u.save()
        return u
