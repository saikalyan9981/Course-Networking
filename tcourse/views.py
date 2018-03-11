from django.shortcuts import render, redirect, get_object_or_404
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from .forms import SignUpForm, StudentSignUpForm, InstSignUpForm, DocumentForm, DeadlineForm,StudentEdit,InstructorEdit,EventEdit, FeedbackForm
from .forms import DriveForm
from django.http import  HttpResponse, Http404
from django.contrib.auth.models import User
from . models import Student, Instructor, Course, Board, Topic, Post , Ipost, Events, Ipost, Feedback, RatingQuestion, RatingAnswer, SubjectiveAnswer, SubjectiveQuestion
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.urls import reverse
from django.views.generic.edit import UpdateView,DeleteView
from django.views import generic
from .str_process import normalize_query, get_query

import re
from django.db.models import Q
# Create your views here.

@login_required
##
# \brief view for homepage of user
def home(request):
    u=request.user
    try: ##<check if user is a student
        stud= u.student.id
    except:
        pass
    else:
        request.session['usr_id']=u.id ##<storing the user_id in a session variable
        request.session['std_id']=stud ##<storing the student_id in a session variable
        return std_home(request)  ##<redirecting to student homepage
    try: ##<check if user is a instructor
        inst= u.instructor.id
    except:
        return redirect('step1') ##<redirect to initiate social media signup
    else:
        request.session['ins_id'] = inst
        request.session['usr_id'] = u.id
        return ins_home(request)

@login_required
def step1(request):
    u = request.user
    return render(request, 'choice.html', {'user': u}) ##<displays to a page to take choice of user (to signup as a student or as an instructor)


@login_required
##
# \brief view for student homepage, passes required parameters to the html template
def std_home(request):
    cstd=Student.objects.get(id=request.session['std_id']) ##<get the logged in Student
    course = cstd.courses.all() ##<the set of Courses taken up by Student
    return render(request, 'std_home.html', {'std': cstd, 'courses': course}) ##<renders the template by passing required parameters

@login_required
##
# \brief view for instructor homepage, passes required parameters to the html template
def ins_home(request):
    cins=Instructor.objects.get(id=request.session['ins_id']) ##<get the logged in Instructor
    course=cins.course_set.all() ##<the set of Courses given by Instructor
    return render(request, 'ins_home.html', {'ins': cins, 'courses': course}) ##<renders the template by passing required parameters

##
# view to redirect to login page
def login_redirect(request):
    return redirect('/login')

##
# \brief view to render signup form
def signup(request):
    if request.method == 'POST':
        form =SignUpForm(request.POST)
        check1 = request.POST.get('is_stud', False) ##<getting the response(signup as student or instructor) from form
        if form.is_valid():
            user = form.save()
            uid = user.id
            if check1 == 'on':
                return redirect('std_signup', pk=uid) ##<redirects to student signup page
            else :
                return redirect('ins_signup', pk=uid)  ##<redirects to instructor signup page
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form}) ##<renders the html template for signup

##
# @param pk
#  represents user_id
# \brief view to render student signup form
def std_signup(request, pk):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            new_student=form.save(commit=False)
            new_student.user = User.objects.get(pk=pk) ##<gets user from user_id
            new_student.save()
            form.save_m2m()
            auth_login(request, new_student.user, backend='django.contrib.auth.backends.ModelBackend') ##<login
            return redirect('home')##<redirected to homepage
        else :
            return HttpResponse("<h1> Invalid form</h1>")
    else:
        form = StudentSignUpForm()
    return render(request, 'signup2.html', {'form': form})

##
# @param pk
#  represents user_id
# \brief view to render instructor signup page
def ins_signup(request,pk):
    if request.method == 'POST':
        form = InstSignUpForm(request.POST)
        if form.is_valid():
            new_inst=form.save(commit=False)
            new_inst.user = User.objects.get(pk=pk) ##<gets user from user_id
            new_inst.save() ##<saving
            form.save_m2m() ##<saves the m2m relations
            auth_login(request, new_inst.user, backend='django.contrib.auth.backends.ModelBackend') ##<login
            return redirect('home') ##<redirecting to homepage after signup
    else:
        form = InstSignUpForm()
    return render(request, 'signup2.html', {'form': form}) ##< rendering instructor signup template

@login_required
##
# @param pk
#  represents course_id
# \brief view to render student homepage of a course
def std_crs(request,pk):
    course = get_object_or_404(Course, pk=pk) ##<gets the Course instance from course_id
    ins = course.teacher.all() ##<gets the list of instructors for this Course
    return render(request, 'std_crs_view.html', {'course': course, 'ins':ins})

@login_required
##
# @param pk
#  represents course_id
# \brief view to render instructor homepage of a course
def ins_crs(request,pk):
    course = get_object_or_404(Course, pk=pk) ##<gets the Course instance from course_id
    ins = course.teacher.all() ##<gets the Course instance from course_id
    return render(request, 'ins_crs_view.html', {'course': course, 'ins':ins})  ##<renders the template by passing required parameters

@login_required
##
# @param pk
#  represents course_id
# \brief view to render student version discussion forum of a course
def std_brd_view(request,pk):
    course = get_object_or_404(Course, pk=pk) ##<gets the Course instance from course_id
    board = get_object_or_404(Board, course=course) ##<gets the corresponding Board of the Course
    topics = board.topic_set.all() ##<gets the list of all Topics in the Board
    return render(request, 'std_board.html', {'course': course, 'board': board, 'topics':topics }) ##<renders the template by passing required parameters

##
# @param pk
#  represents course_id
# \brief view for  student version of search results page
def bsearch(request,pk):
    course = get_object_or_404(Course, pk=pk) ##<gets the Course instance from course_id
    board = get_object_or_404(Board, course=course) ##<gets the corresponding Board of the Course
    topics = board.topic_set.all() ##<gets the list of all Topics in the Board
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q'] ##<gets the search string from form

        entry_query = get_query(query_string, ['name', 'brief', ]) ##<processes string to remove quotations, whitespaces, tabs and gets a list

        found_entries = topics.filter(entry_query).order_by('-created_at') ##<search results - list of Topics

    return render(request,'search/search_res.html',
                              {'query_string': query_string, 'src_res': found_entries, 'course': course, 'board': board}) ##<template rendering

##
# @param pk
#  represents course_id
# \brief view for instructor version of search results page
def ibsearch(request,pk):
    course = get_object_or_404(Course, pk=pk) ##<gets the Course instance from course_id
    board = get_object_or_404(Board, course=course)  ##<gets the corresponding Board of the Course
    topics = board.topic_set.all() ##<gets the list of all Topics in the Board
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q'] ##<gets the search string from form

        entry_query = get_query(query_string, ['name', 'brief', ]) ##<processes string to remove quotations, whitespaces, tabs and gets a list

        found_entries = topics.filter(entry_query).order_by('-created_at') ##<search results - list of Topics

    return render(request,'search/isearch_res.html',
                              {'query_string': query_string, 'src_res': found_entries, 'course': course, 'board': board}) ##<template rendering


@login_required
##
# @param pk
#  represents course_id
# \brief view for instructor version of  discussion forum page
def ins_brd_view(request, pk):
    course = get_object_or_404(Course, pk=pk) ##<gets the Course instance from course_id
    board = get_object_or_404(Board, course=course) ##<gets the corresponding Board of the Course
    topics = board.topic_set.all()  ##<gets the list of all Topics in the Board
    return render(request, 'ins_board.html', {'course': course, 'board': board, 'topics':topics }) ##<template rendering

@login_required
##
# @param pk
#  represents topic_id
# \brief view for student version of a particular topic page
def topic_view(request,pk):
    topic = get_object_or_404(Topic, pk=pk) ##<gets Topic instance from topic_id
    board = topic.board ##<gets the corresponding Board of the Topic
    course = board.course ##<gets the Course instance of the Board
    posts = topic.post_set.all() ##<gets the list of all Posts for this Topic
    iposts = topic.ipost_set.all() ##<gets the list of all Iposts(replies of instructors) for this Topic
    return render(request, 'topic_view.html', {'course': course, 'board': board, 'topic': topic, 'posts':posts, 'iposts':iposts }) ##<template rendering

@login_required
##
# @param pk
#  represents topic_id
# \brief view for instructor version of a particular topic page
def topic_iview(request,pk):
    topic = get_object_or_404(Topic, pk=pk)  ##<gets Topic instance from topic_id
    board = topic.board ##<gets the corresponding Board of the Topic
    course = board.course ##<gets the Course instance of the Board
    posts = topic.post_set.all() ##<gets the list of all Posts for this Topic
    iposts = topic.ipost_set.all() ##<gets the list of all Iposts(replies of instructors) for this Topic
    return render(request, 'topic_iview.html', {'course': course, 'board': board, 'topic': topic, 'posts':posts, 'iposts':iposts }) ##<template rendering

@login_required
##
# @param pk
#  represents course_id
# \brief view for form to post a new Topic (question)
def new_topic(request,pk):
    course = get_object_or_404(Course, pk=pk) ##<gets the Course instance from course_id
    board = get_object_or_404(Board, course=course) ##<gets the corresponding Board of the Course
    if request.method == 'POST':
        name = request.POST['name']
        brief = request.POST['brief'] ##<gets fields from form
        user = User.objects.get(id=request.session['usr_id']) ##<gets User from session var
        topic = Topic.objects.create( ##<creating new Topic instance
            name=name,
            brief=brief,
            board=board,
            starter=user,
        )
        return redirect('std_brd_view', pk=course.id) ##<redirecting to student discussion forum page
    return render(request, 'new_topic.html', {'course': course, 'board':board}) ##<rendering template

@login_required
##
# @param pk
#  represents topic_id
# \brief view for form to post a new Post (reply)
def new_post(request,pk):
    topic = get_object_or_404(Topic, pk=pk) ##<gets Topic instance from topic_id
    board = topic.board ##<gets the corresponding Board of the Topic
    course= board.course  ##<gets the Course instance of the Board
    user = User.objects.get(id=request.session['usr_id']) ##<gets User from session var
    if request.method == 'POST':
        message = request.POST['message'] ##<gets message field from form
        post = Post.objects.create( ##<creates new Post instance
            message=message,
            author =user,
            topic=topic,
        )
        return redirect('topic_view', pk=topic.id) ##<redirects to the page of corresponding topic
    return render(request, 'reply.html', {'course': course, 'board':board, 'topic':topic}) ##<template rendering

@login_required
##
# @param pk
#  represents topic_id
# \brief view for form to post a new Ipost (reply)
def new_ipost(request,pk):
    topic = get_object_or_404(Topic, pk=pk) ##<gets Topic instance from topic_id
    board = topic.board ##<gets the corresponding Board of the Topic
    course= board.course ##<gets the Course instance of the Board
    user = User.objects.get(id=request.session['usr_id']) ##<gets User from session var
    if request.method == 'POST':
        message = request.POST['message'] ##<gets message field from form
        post = Ipost.objects.create( ##<creates new Ipost instance
            message=message,
            author =user,
            topic=topic,
        )
        return redirect('topic_iview', pk=topic.id) ##<redirects to the page of corresponding topic
    return render(request, 'ireply.html', {'course': course, 'board':board, 'topic':topic}) ##<template rendering

@login_required
##
# @param pk
#  represents course_id
# \brief view for instructor's page of course resources
def ins_res(request,pk):
    course = get_object_or_404(Course, pk=pk) ##<gets the Course instance from course_id
    docs = course.document_set.all() ##<set of all Documents for that course
    return render(request, 'ins_res_view.html', {'course': course, 'docs':docs}) ##<template rendering

@login_required
##
# @param pk
#  represents course_id
# \brief view for students's page of course resources
def std_res(request,pk):
    course = get_object_or_404(Course, pk=pk) ##<gets the Course instance from course_id
    docs = course.document_set.all() ##<set of all Documents for that course
    return render(request, 'std_res_view.html', {'course': course, 'docs':docs}) ##<template rendering

@login_required
##
# \brief view for Personal Drive
def personaldrive(request):
    user = request.user ##<gets the User instance
    docs = user.personaldrive_set.all()##<set of all Documents of that user
    return render(request, 'personaldrive/drive_view.html', {'user':user, 'docs':docs})##<template rendering

@login_required
##
# \brief view for Uploading files in drive
def drive_upload(request):
    user = request.user ##<gets the User instance
    if request.method == 'POST':
        form = DriveForm(request.POST, request.FILES)
        if form.is_valid():
            new_doc = form.save(commit=False)#<saving the form with null user as new_doc
            new_doc.user = user ##<sets user field
            new_doc.save()##<saves the new_doc
            return redirect('personaldrive')##<redirects to the page of personal drive
    else:
        form = DriveForm()##<sets form
    return render(request, 'personaldrive/drive_upload.html', {'form': form, 'user': user})##<template rendering of form



@login_required
##
# @param pk
#  represents course_id
# \brief view for resource upload
def new_res(request,pk):
    course = get_object_or_404(Course, pk=pk) ##<gets the Course instance from course_id
    board = get_object_or_404(Board, course=course) ##<gets the Board instance from course
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            new_doc = form.save(commit=False)
            new_doc.course= course
            new_doc.save()
            return redirect('ins_res', pk=course.pk) ##<redirected to instructor's resource page
    else:
        form = DocumentForm()
    return render(request, 'res_upload.html', {'form': form, 'course': course, 'board':board}) ##<template rendering

@login_required
##
# @param pk
#  represents course_id
# \brief view to add Deadline in the Events Class
def addDeadline(request,pk):
    course=get_object_or_404(Course, pk=pk)##<get the course instance from its pk
    if request.method =='POST':
       form = DeadlineForm(request.POST)
       if form.is_valid():
           name = request.POST['name']##<gets name field from form
           deadline_date = request.POST['deadline_date']##<gets deadline_date field from form
           deadline_time = request.POST['deadline_time']##<gets deadline_time from form
           description = request.POST['description']##<gets description from form
           a=Events(course=Course.objects.get(id=pk),name=name,deadline_date=deadline_date,deadline_time=deadline_time,description=description)#<intializing event named 'a'
           a.save()#<saving event
           return redirect('ins_crs', pk=pk)##<redirects to the course homepage of instructor
    else:
        form = DeadlineForm()##<sets form
        context = {'form': form,'course':course}
    return render(request,'addEvent.html',context)##<template rendering of form

@login_required
##
# @param pk
#  represents events_id
# @param id
#  represents course_id
# \brief view to delete Deadline in the Events Class
def delete_event(request, pk , id):
    event = Events.objects.get(pk=pk)##<get the event instance from its pk
    event.delete()##<delete the event
    return redirect('ins_crs',pk=id)##<redirects to the course homepage of instructor

@login_required
##
# @param pk
#  represents events_id
# @param id
#  represents course_id
# \brief view to edit Deadline in the Events Class
def edit_event(request,pk,id):
    event = Events.objects.get(pk=pk)##<get the event instance from its pk
    if request.method == 'POST':
        form = EventEdit(request.POST,instance=event)##<gets form with event instance
        if form.is_valid():
            form.save()##<saves form
            return redirect('ins_crs', pk=id)##<redirects to the course homepage of instructor
    else:
        form = EventEdit(instance=event)##<initiating the form
        args = {'form': form}
        return render(request, 'edit_event.html', args)##<template rendering of form

@login_required
##
# @param pk
#  represents student_id , can be none
# \brief view to view Student profile
def view_studentprofile(request,pk=None):
    if pk:
        user1=Student.objects.get(pk=pk)##<get the student instance from its pk
    else:
        user1= request.user.student##<get the student instance from user
    return render(request,'profile.html',{'user1':user1})##<template rendering

##
# \brief view to generate student's timetable

@login_required
def ttb(request):
    cstd = Student.objects.get(id=request.session['std_id'])
    course = cstd.courses.all()
    dict={}
    for crs in course:
        slt=crs.slot.all()
        for slot in slt:
            dict[slot.name]=crs.name
    return render(request, 'std-ttb.html', {'dict': dict})

@login_required
##
# @param pk
#  represents instructor_id , can be none
# \brief view to view Instructor profile
def view_instructorprofile(request,pk=None):
    if pk:
        user1=Instructor.objects.get(pk=pk)##<get the Instructor instance from its pk
    else:
        user1= request.user.instructor##<get the Instructor instance from user
    return render(request,'profile.html',{'user1':user1})##<template rendering

@login_required
##
# |brief view to edit Instructor profile
def insedit_profile(request):
    if request.method == 'POST':
        form = InstructorEdit(request.POST,request.FILES, instance=request.user.instructor)##<gets form with instructor instance
        if form.is_valid():
            form.save()##<saving the form
            return redirect('withoutidinsprofile')##<redirecting to profile
    else:
        form = InstructorEdit(instance=request.user.instructor)##<intialising student edit form
        args = {'form': form}
        return render(request, 'profile/edit_profile.html', args)##<template rendering for form

@login_required
##
# |brief view to edit student profile
def edit_profile(request):
    if request.method == 'POST':
        form = StudentEdit(request.POST,request.FILES, instance=request.user.student)##<gets form with student instance
        if form.is_valid():
            form.save()##<saving the form
            return redirect('withoutidstprofile')##<redirecting to profile
    else:
        form = StudentEdit(instance=request.user.student)##<intialising student edit form
        args = {'form': form}
        return render(request, 'profile/edit_profile.html', args)##<template rendering for form

@login_required
##
# @param pk
#  represents event_id
# \brief view to get event info
def eventdetails(request,pk):
    event = get_object_or_404(Events, pk=pk)##<get the Events instance from its pk
    return render(request, 'eventdetail.html', {'event': event})##<rendering template

#Feedback
@login_required
##
# @param pk
# Represents instructor's id
# \brief Instructor add feedback form view
def addFeedback(request, pk):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback_name = request.POST['feedback_name']##<gets the feedback's name
            deadline_date = request.POST['deadline_date']##<gets the deadline data
            deadline_time = request.POST['deadline_time']##<gets the deadline time
            f = Feedback(feedback_name=feedback_name,deadline_time=deadline_time,deadline_date=deadline_date,course=Course.objects.get(id=pk))
            f.save()
            i = request.POST['ratedQuestions']
            l = 0 
            while l < int(i): ##< loop to get all the rating questions. 
                l = l+1
                question = request.POST['rated'+str(l)]
                x = RatingQuestion(question=question,feedback=f)
                x.save()
            i = request.POST['subjectiveQuestions']
            l = 0
            while l < int(i): ##< loop to get all the subjective questions. 
                l = l+1
                question = request.POST['subjective'+str(l)]
                x = SubjectiveQuestion(question=question,feedback=f)
                x.save()
            return redirect('ins_crs', pk=pk)
    else:
        form = FeedbackForm()
        context = {'form': form, 'pk': pk}
    return render(request, 'addFeedback.html',context)

@login_required
##
# @param pk
# Represents question's id
# \brief view for subjective feedback(instructor's, after data is acquired)
def subjectiveFeedback(request, pk):
    question = SubjectiveQuestion.objects.get(id=pk)
    context = {'question':question}
    return render(request, 'subjectiveFeedback.html',context)

@login_required
##
# @param pk
# Represents quetion's id
# \brief view for rating feedback(instructor's, after data is acquired)
def ratingFeedback(request, pk):
    question = RatingQuestion.objects.get(id=pk)
    import matplotlib
    from matplotlib.dates import DateFormatter
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    data=[0,0,0,0,0]
    for answer in question.ratinganswer_set.all(): 
        data[answer.answer_rated-1] = data[answer.answer_rated-1]+1
    print(data)
    fig = Figure(figsize=(2,2))
    ax=fig.add_subplot(1,1,1)
    cols = ['red','orange','yellow','green','blue','purple','indigo']*10
    ind = [1,2,3,4,5]
    cols = cols[0:len(ind)]
    ax.bar(ind, data,color=cols)
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

@login_required
##
# @param pk
# Represents feedback's id
# \brief student's feedback view
def submitFeedback(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    course = feedback.course
    # feedback_name = feedback.feedback_name
    cstd = Student.objects.get(id=request.session['std_id'])
    rquestions = feedback.ratingquestion_set.all()
    squestions = feedback.subjectivequestion_set.all()
    a="rating"
    b="subjective"
    if request.method == 'POST':
        for question in rquestions: ##< loop to get all the rating answers
            answer = request.POST["rating"+str(question.id)]
            x = RatingAnswer(question=question, answer_rated=answer, student = cstd)
            x.save()
        for question in squestions: ##< loop to get all the subjective answers
            answer = request.POST["subjective"+str(question.id)]
            x = SubjectiveAnswer(question=question, answer=answer, student=cstd)
            x.save()
        return redirect('home')
    else:
        context = { 'feedback':feedback, 'pk' : pk, 'course':course}
    return render(request, 'submitFeedback.html', context)

@login_required
##
# @param pk
# Represents course's id
# \brief instructor view of collected answers to feedback forms
def viewFeedback(request, pk):
    cins = Instructor.objects.get(id=request.session['ins_id'])
    course = Course.objects.get(id=pk)
    context = {'instructor':cins, 'pk': pk, 'course': course}
    return render(request, 'viewFeedback.html', context)
@login_required
##
# @param pk
#  represents course_id
# \brief view to get course info
def courseinfo(request,pk):
    course= get_object_or_404(Course,pk=pk)##<get the Course instance from its pk
    ins= course.teacher.all()##<list of all instructors of that course
    args = {'ins':ins,'course':course}
    return render(request, 'courseinfo.html', args)##<template rendering

