"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from tcourse import views as tc_views
from . import settings
from django.views.static import serve
from updown.views import AddRatingFromModel
from tcourse.models import Post

urlpatterns = [
    url(r'^$', tc_views.home, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^signup/$', tc_views.signup, name='signup'),
    url(r'^step1/$', tc_views.step1, name='step1'),
    url(r'^signup/std_signup/(?P<pk>\d+)/$', tc_views.std_signup, name='std_signup'),
    url(r'^signup/ins_signup/(?P<pk>\d+)/$', tc_views.ins_signup, name='ins_signup'),
    url(r'^logout/$', auth_views.logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # <--
    url(r'^std_crs/(?P<pk>\d+)/$', tc_views.std_crs, name='std_crs'),
    url(r'^std_crs/(?P<pk>\d+)/res$', tc_views.std_res, name='std_res'),
    url(r'^std_ttb/$', tc_views.ttb, name='std_ttb'),
    url(r'^blog_search/(?P<pk>\d+)/$', tc_views.bsearch, name='blog_search'),
    url(r'^blog_isearch/(?P<pk>\d+)/$', tc_views.ibsearch, name='blog_isearch'),
    url(r'^ins_crs/(?P<pk>\d+)/$', tc_views.ins_crs, name='ins_crs'), #Istructor's
    url(r'^ins_crs/(?P<pk>\d+)/res/new$', tc_views.new_res, name='new_res'), #Istructor's
    url(r'^ins_crs/(?P<pk>\d+)/res$', tc_views.ins_res, name='ins_res'), #Istructor's
    url(r'^board/(?P<pk>\d+)/$', tc_views.std_brd_view, name='std_brd_view'),
    url(r'^iboard/(?P<pk>\d+)/$', tc_views.ins_brd_view, name='ins_brd_view'),
    url(r'^board/(?P<pk>\d+)/new$', tc_views.new_topic, name='new_topic'), #course_id # new topic in the board
    url(r'^topic/(?P<pk>\d+)/view$', tc_views.topic_view, name='topic_view'),
    url(r'^topic/(?P<pk>\d+)/iview$', tc_views.topic_iview, name='topic_iview'),
    url(r'^topic/(?P<pk>\d+)/new$', tc_views.new_post, name='new_post'),  #topic_id # new reply for the topic
    url(r'^topic/(?P<pk>\d+)/inew$', tc_views.new_ipost, name='new_ipost'),  #topic_id # new ins reply for the topic
    
####instructor
  #  url(r'^course_home/(?P<pk>\d+)/$', tc_views.course_home, name='course_home'),
   # url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
   url(r'^instructor/(?P<pk>\d+)/addDeadline$', tc_views.addDeadline, name='addDeadline'),
    url(r'^event/delete/(?P<pk>\d+)/(?P<id>\d+)$',tc_views.delete_event,name='deleteevent'),
    url(r'^event/edit/(?P<pk>\d+)/(?P<id>\d+)$', tc_views.edit_event, name='editevent'),

    ####student profile
    url(r'^student/profile/$', tc_views.view_studentprofile, name='withoutidstprofile'),
    url(r'^student/profile/(?P<pk>\d+)/$',tc_views.view_studentprofile,name='stprofile'),
    ####instructor profile
    url(r'^instructor/profile/$', tc_views.view_instructorprofile, name='withoutidinsprofile'),
    url(r'^instructor/profile/(?P<pk>\d+)/$',tc_views.view_instructorprofile,name='insprofile'),
    url(r'^instructor/profile/edit/$', tc_views.insedit_profile, name='insedprofile'),

    # feedback urls:
    url(r'^instructor/(?P<pk>\d+)/addFeedback$', tc_views.addFeedback, name='addFeedback'),
    url(r'^subjectiveFeedback/(?P<pk>\d+)$', tc_views.subjectiveFeedback, name='subjectiveFeedback'),
    url(r'^ratingFeedback/(?P<pk>\d+)$', tc_views.ratingFeedback,name='ratingFeedback'),
    url(r'^submitFeedback/(?P<pk>\d+)$', tc_views.submitFeedback, name='submitFeedback'),
    url(r'^viewFeedback/(?P<pk>\d+)$', tc_views.viewFeedback, name='viewFeedback'),

    ###calendar
    url(r'^eventcalendar/',include('eventcalendar.urls')),

    ##eventdetails
    url(r'^eventdetail/(?P<pk>\d+)$',tc_views.eventdetails,name="eventdetail"),
    url(r'^student/profile/edit/$', tc_views.edit_profile, name='stedprofile'),
    #url(r'^student/profile/(?P<pk>\d+)/edit/$', tc_views.edit_studentprofile, name='stedprofile'),
    url(r"^(?P<object_id>\d+)/rate/(?P<score>[\d\-]+)$", AddRatingFromModel(), {
        'app_label': 'tcourse',
        'model': 'Post',
        'field_name': 'rating',
    }, name="post_rating"),
    url(r'^courseinfo/(?P<pk>\d+)/$',tc_views.courseinfo,name='courseinfo'),
    url(r'^personaldrive/$',tc_views.personaldrive,name='personaldrive'),
    url(r'^drive_upload/$',tc_views.drive_upload,name='drive_upload'),

]
if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]