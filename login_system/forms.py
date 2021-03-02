from django import forms
from django.forms import ModelForm
from alldata.models import *


class MyUserCreateForm(ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    password_copy = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['email','password']

class QuizCreateForm(forms.ModelForm):
    name = forms.CharField(required=True)
    description = forms.CharField(required=True)
    open_time = forms.CharField(required=True)#forms.DateTimeField(required=True)
    close_time = forms.CharField(required=True)#forms.DateTimeField(required=True)
    time_limit = forms.IntegerField(required=True)
    max_point = forms.IntegerField(required=True)
    # module = forms.ModelChoiceField(queryset=Coursepagemodule.objects.filter(owner=user))
    # module = forms.IntegerField(required=True)
    def __init__(self, *args, **kwargs):
        coursesection_id = kwargs.pop('section_id','')
        super(QuizCreateForm, self).__init__(*args, **kwargs)
        self.fields['module'] = forms.ModelChoiceField(queryset=Coursepagemodule.objects.filter(coursesection_sectionid = coursesection_id).order_by('order').all())
    
    class Meta:
        model = Quiz
        fields = ['name','description', 'open_time', 'close_time', 'time_limit', 'max_point']