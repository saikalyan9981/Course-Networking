from datetime import datetime,date
from django.shortcuts import render_to_response
#import calendar
from tcourse.models import Student, Instructor, Course, Board, Topic, Post , Events,Feedback
from django.utils.html import conditional_escape as esc
from django.utils.safestring import mark_safe
from itertools import groupby
from itertools import chain
from calendar import HTMLCalendar,monthrange

class ContestCalendar(HTMLCalendar):

    def __init__(self, pContestEvents):
        super(ContestCalendar, self).__init__()
       # print (pContestEvents)
        self.contest_events = self.group_by_day(pContestEvents)
        # print (self.contest_events)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.contest_events:
                cssclass += ' filled'
                body = []
               # print (self.contest_events[day])
                for contest in self.contest_events[day]:
                    #body.append('<a href="{% url "eventdetail" contest.id %}">')
                    body.append('<a href="%s">' % contest.get_absolute_url())
                    body.append(esc(contest.name))
                    body.append('</a><br/>')
                return self.day_cell(cssclass, '<div class="dayNumber">%d</div> %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, '<div class="dayNumber">%d</div>' % day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(ContestCalendar, self).formatmonth(year, month)

    def group_by_day(self, pContestEvents):
        field = lambda contest: contest.deadline_date.day
        #print (field)
        return dict(
            [(day, list(items)) for day, items in groupby(pContestEvents, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)

def named_month(pMonthNumber):
    """
    Return the name of the month, given the month number
    """
    return date(1900, pMonthNumber, 1).strftime('%B')




def home(request):
    """
    Show calendar of events this month
    """
    lToday = datetime.now()
    return calendar(request, lToday.year, lToday.month)

def calendar(request, pYear, pMonth):
    """
    Show calendar of events for specified month and year
    """
    lYear = int(pYear)
    lMonth = int(pMonth)
    lCalendarFromMonth = datetime(lYear, lMonth, 1)
    lCalendarToMonth = datetime(lYear, lMonth, monthrange(lYear, lMonth)[1])
    user=request.user
    feed=Feedback.objects.filter(course__in = request.user.student.courses.all(),deadline_date__gte=lCalendarFromMonth, deadline_date__lte=lCalendarToMonth)
    lContestEvents = Events.objects.filter(course__in = request.user.student.courses.all(),deadline_date__gte=lCalendarFromMonth, deadline_date__lte=lCalendarToMonth)

    ########
    #print (request.user.student.pk)
    #print (lContestEvents)
    lCalendar = ContestCalendar(lContestEvents).formatmonth(lYear, lMonth)
    lPreviousYear = lYear
    lPreviousMonth = lMonth - 1
    if lPreviousMonth == 0:
        lPreviousMonth = 12
        lPreviousYear = lYear - 1
    lNextYear = lYear
    lNextMonth = lMonth + 1
    if lNextMonth == 13:
        lNextMonth = 1
        lNextYear = lYear + 1
    lYearAfterThis = lYear + 1
    lYearBeforeThis = lYear - 1

    return render_to_response('eventcalendar/home.html', {'Calendar' : mark_safe(lCalendar),
                                                       'Month' : lMonth,
                                                       'MonthName' : named_month(lMonth),
                                                       'Year' : lYear,
                                                       'PreviousMonth' : lPreviousMonth,
                                                       'PreviousMonthName' : named_month(lPreviousMonth),
                                                       'PreviousYear' : lPreviousYear,
                                                       'NextMonth' : lNextMonth,
                                                       'NextMonthName' : named_month(lNextMonth),
                                                       'NextYear' : lNextYear,
                                                       'YearBeforeThis' : lYearBeforeThis,
                                                       'YearAfterThis' : lYearAfterThis,
                                                        'user':user
                                                   },request)
