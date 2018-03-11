from django.contrib import admin
from .models import Instructor, Student, Course, Board, Topic,Events,Slot, Feedback, RatingQuestion, SubjectiveQuestion, SubjectiveAnswer, RatingAnswer
# Register your models here.
admin.site.register(Instructor)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Events)
admin.site.register(Slot)

#feedback stuff
admin.site.register(Feedback)
admin.site.register(RatingQuestion)
admin.site.register(SubjectiveQuestion)
admin.site.register(SubjectiveAnswer)
admin.site.register(RatingAnswer)
