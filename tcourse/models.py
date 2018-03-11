import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from updown.fields import RatingField
import os

##
# one-one extension of django's User model, for instructors
class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) ##<the corresponding User instance whose extension is this instance
    fullname = models.CharField(max_length=30,default='',blank=True )
    description = models.CharField(max_length=150,default='',blank=True )
    is_student= models.BooleanField(default=False)
    website = models.URLField(default='',blank=True )
    phone = models.IntegerField(null='True')
    city = models.CharField(max_length=100, default='',blank=True)
    image = models.ImageField(upload_to='documents/',default = 'default_user.png',blank=True )  ##<profile picture

    ##
    # @param self The object pointer.
    # @returns name of the image file
    @property
    def filename(self):
        return os.path.basename(self.image.name)

    ##
    # @param self The object pointer.
    # @returns name of user
    def __str__(self):
        return self.user.username


    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('insprofile', args=[str(self.id)])
##
# slot model used in timetable
class Slot(models.Model):
    name = models.CharField(max_length=30, default='')
    description=models.CharField(max_length=30, default='') ##<description of the timeslot ie day and time

    ##
    # @param self The object pointer.
    # @returns name of the slot
    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    teacher = models.ManyToManyField(Instructor) ##<the corresponding Instructor instance
    slot= models.ManyToManyField(Slot) ##<the @see Slot (s) for this course

    ##
    # @param self The object pointer.
    # @returns name of course
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('courseinfo', args=[str(self.id)])

##
# one-one extension of django's User model, for students
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) ##<the corresponding User instance whose extension is this instance
    fullname = models.CharField(max_length=30,default='',blank=True )
    description = models.CharField(max_length=150,default='',blank=True )
    courses= models.ManyToManyField(Course)  ##<the @see Course (s) taken up by the Student
    website = models.URLField(default='',blank=True )
    phone = models.IntegerField(default=0 )
    city = models.CharField(max_length=100, default='',blank=True )
    image = models.ImageField(upload_to='documents/',default = 'default_user.png',blank=True ) ##<profile picture
    is_student= models.BooleanField(default=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('stprofile', args=[str(self.id)])

    ##
    # @param self The object pointer.
    # @returns name of the image file
    @property
    def filename(self):
        return os.path.basename(self.image.name)

    ##
    # @param self The object pointer.
    # @returns name of user
    def __str__(self):
        return self.user.username

##
# the model for discussion forum
class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    course = models.ForeignKey(Course) ##<the corresponding @see Course

    ##
    # @param self The object pointer.
    # @returns name of board
    def __str__(self):
        return self.name

##
# model for question in discussion forum
class Topic(models.Model):
    name = models.CharField(max_length=300,default='') ##<the content of the question
    brief = models.CharField(max_length=30, default='') ##<brief description of the question
    created_at = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board) ##<the @see Board in which this question is present
    starter = models.ForeignKey(User, on_delete=models.CASCADE) ##<User who posted this question

    ##
    # @param self The object pointer.
    # @returns name of topic
    def __str__(self):
        return self.name

##
# model for instructor's reply in discussion forum
class Ipost(models.Model):       #replies
    message = models.TextField(max_length=4000) ##<the matter of reply
    topic = models.ForeignKey(Topic) ##<the @see Topic for which this is a reply
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = RatingField(can_change_vote=True) ##< sores number upvotes, downvotes; 1 for each UPVOTE and -1 for each DOWNVOTE
    def __str__(self):
        return self.message

##
# model for student's reply in discussion forum
class Post(models.Model):
    message = models.TextField(max_length=4000) ##<the matter of reply
    topic = models.ForeignKey(Topic) ##<the @see Topic for which this is a reply
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = RatingField(can_change_vote=True) ##< stores number upvotes, downvotes; 1 for each UPVOTE and -1 for each DOWNVOTE
    def __str__(self):
        return self.message

    ##
    # Meta class for ordering based on number of likes
    class Meta:
        ordering = ['rating_likes']

##
# model for file storage
class Document(models.Model):
    description = models.CharField(max_length=255, default='', blank=True) ##<description of the document
    document = models.FileField(upload_to='documents/') ##<the file
    course = models.ForeignKey(Course,on_delete=models.CASCADE) ##<the corresponding @see Course
    uploaded_at = models.DateTimeField(auto_now_add=True)

    @property
    def filename(self):
        return os.path.basename(self.document.name)

##
# model for personal drive of user
class Personaldrive(models.Model):
    description = models.CharField(max_length=255, default='', blank=True) ##<description of the document
    document = models.FileField(upload_to='drive/',null=True) ##<the file
    user = models.ForeignKey(User, on_delete=models.CASCADE) ##<the corresponding User
    uploaded_at = models.DateTimeField(auto_now_add=True)
    @property
    def filename(self):
        return os.path.basename(self.document.name)

##
# model for Events of a course
class Events(models.Model):
    name = models.CharField(max_length=50) ##<exam or submission
    course= models.ForeignKey(Course,on_delete=models.CASCADE) ##< the corressponding @see Course instance
    deadline_date = models.DateField(default=datetime.date.today)
    deadline_time = models.TimeField(default='23:59')
    description = models.CharField(max_length=255, blank=True)


    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('eventdetail', args=[str(self.id)])

    ##
    # @param self The object pointer.
    # @returns name of event
    def __str__(self):
        return self.name

    ##
    # @param self The object pointer.
    # @returns if the event is due or not
    def is_due(self):
        if self.deadline_date > datetime.datetime.now().date():
            return True
        if self.deadline_date >= datetime.datetime.now().date():
            if self.deadline_time >= datetime.datetime.now().time():
                return True
        return False

    ##
    # Meta class for ordering based on deadline_time
    class Meta:
        ordering = ['deadline_time']

##
# The model for feedback. Doesn't contain answers.
class Feedback(models.Model):
    feedback_name = models.CharField(max_length = 20,default='')
    deadline_date = models.DateField(default=datetime.date.today)
    deadline_time = models.TimeField(default='23:59')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default='') ##< the @see Course of this feeback
    def __str__(self):
        return self.feedback_name

    ##
    # @param self The object pointer.
    # @returns if this feedback is due or not
    def is_due(self):
        if self.deadline_date >= datetime.datetime.now().date():
            if self.deadline_time >= datetime.datetime.now().time():
                return True
        return False

##
# The model for rating questions
class RatingQuestion(models.Model):
    question = models.CharField(max_length = 150,default="")
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE) ##< the @see Feedback in which this is a question
    def __str__(self):
        return self.question

##
# The model for rating answers
class RatingAnswer(models.Model):
    question = models.ForeignKey(RatingQuestion, on_delete=models.CASCADE) ##< the @see RatingQuestion for which this is answer
    answer_rated = models.IntegerField(default = 3)
    student = models.ForeignKey(Student) ##< the @see Student who gave this answer

##
# The model for subjective questions
class SubjectiveQuestion(models.Model):
    question = models.CharField(max_length = 150,default="")
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE) ##< the @see Feedback in which this is a question
    ## 
    # @param self the object pointer
    # @returns the qusetion
    def __str__(self):
        return self.question

##
# The model for subjective answers
class SubjectiveAnswer(models.Model):
    question = models.ForeignKey(SubjectiveQuestion, on_delete=models.CASCADE) ##< the @see SubjectiveQuestion for which this is answer
    answer = models.CharField(max_length= 300, default = "")
    student = models.ForeignKey(Student) ##< the @see Student who gave this answer
