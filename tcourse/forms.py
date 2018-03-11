from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, Instructor, Document ,Events, Feedback, Course,Personaldrive
import datetime
from django_countries.widgets import CountrySelectWidget

##
# The form for user signup, the fields in the Meta class are shown in the form
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    #check = forms.BooleanField(required=True, initial=True, label='Signup as Student')
    class Meta:
        model = User ##<the model used in this form
        fields = ('username', 'email', 'password1', 'password2')
##
# The form for student signup, the fields in the Meta class are shown in the form
class StudentSignUpForm(forms.ModelForm):
    class Meta:
        model=Student ##<the model used in this form
        fields=('fullname', 'description', 'courses')
##
# The form for Instructor signup, the fields in the Meta class are shown in the form
class InstSignUpForm(forms.ModelForm):
    class Meta:
        model = Instructor ##<the model used in this form
        fields = ('fullname', 'description')

##
# The form for Document upload, the fields in the Meta class are shown in the form
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document ##<the model used in this form
        fields = ('description', 'document', )

##
# The form for Drive upload, the fields in the Meta class are shown in the form
class DriveForm(forms.ModelForm):
    class Meta:
        model = Personaldrive ##<the model used in this form
        fields = ('description', 'document', )

##
# The form for Adding events, the fields in the Meta class are shown in the form
class DeadlineForm(forms.ModelForm):
    class Meta:
        model = Events ##<the model used in this form
        fields=('name','deadline_date', 'deadline_time','description' )

##
# The form for Editting Instructor profile, the fields in the Meta class are shown in the form
class InstructorEdit(forms.ModelForm):
    class Meta:
        model = Instructor ##<the model used in this form
        fields=('fullname','description','website','phone','city','image')
      #  widgets = {'country': CountrySelectWidget()}

##
# The form for Editing Student profile, the fields in the Meta class are shown in the form
class StudentEdit(forms.ModelForm):
    class Meta:
        model = Student ##<the model used in this form
        fields=('fullname','description','website','phone','city','image')
      #  widgets = {'country': CountrySelectWidget()}


##
# The form for Ediiting event, the fields in the Meta class are shown in the form
class EventEdit(forms.ModelForm):
    class Meta:
        model = Events ##<the model used in this form
        fields=('name','deadline_date', 'deadline_time','description' )

##
# Form for feedback, the fields in the Meta class are shown in the form
class FeedbackForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(),empty_label=None,
                                                        widget=forms.Select(attrs={'class':'form-control'}))
    feedback_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class':'form-control',
                                                                                'placeholder':'Enter feedback Name'}))
    deadline_date = forms.DateField(initial=datetime.date.today)
    deadline_time = forms.TimeField(initial="23:59")

