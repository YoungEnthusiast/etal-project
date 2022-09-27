# cal/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from account.models import Collab
from calendarapp.models import EventMember, Event
from calendarapp.utils import Calendar
from calendarapp.forms import EventForm, AddMemberForm

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = "login"
    model = Event
    template_name = "calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context

@login_required(login_url="login")
def create_event(request, id1, **kwargs):
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data["title"]
        description = form.cleaned_data["description"]
        location = form.cleaned_data["location"]
        link = form.cleaned_data["link"]
        start_time = request.GET.get('startdate')
        end_time = form.cleaned_data["end_time"]
        reminder = form.cleaned_data["reminder"]
        Event.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            location=location,
            link=link,
            start_time=start_time,
            end_time=end_time,
            reminder=reminder,
        )
        return HttpResponseRedirect(reverse("calendarapp:schedules-initiated"), 1)
    return render(request, "event.html", {"form": form})

def addTask(request, id1, **kwargs):
    collab = Collab.objects.get(id=id1)
    if collab.researcher == request.user:
        form = TaskForm()
        if request.method == 'POST':
            form = TaskForm(request.POST, request.FILES, None)
            if form.is_valid():
                form.save(commit=False).collab=collab
                form.save()
                reg = Task.objects.all()[0]
                reg.serial = reg.id
                reg.save()

                messages.info(request, "The task has been added successfully")
                return redirect('tasks_initiated', id1)
            else:
                messages.error(request, "Please review form input fields below")
        return render(request, 'account/add_task.html', {'form':form, 'collab':collab})
    elif request.user in collab.collaborators.all():
        form = TaskForm()
        if request.method == 'POST':
            form = TaskForm(request.POST, request.FILES, None)
            if form.is_valid():
                form.save(commit=False).collab=collab
                form.save()
                reg = Task.objects.all()[0]
                reg.serial = reg.id
                reg.save()

                messages.info(request, "The task has been added successfully")
                return redirect('tasks_accepted', id1)
            else:
                messages.error(request, "Please review form input fields below")
        return render(request, 'account/add_task.html', {'form':form, 'collab':collab})

    else:
        return redirect('collab')


class EventEdit(generic.UpdateView):
    model = Event
    fields = ["title", "description", "start_time", "end_time"]
    template_name = "event.html"

@login_required(login_url="join")
def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    eventmember = EventMember.objects.filter(event=event)
    context = {"event": event, "eventmember": eventmember}
    return render(request, "event-details.html", context)


def add_eventmember(request, event_id):
    forms = AddMemberForm()
    if request.method == "POST":
        forms = AddMemberForm(request.POST)
        if forms.is_valid():
            member = EventMember.objects.filter(event=event_id)
            event = Event.objects.get(id=event_id)
            if member.count() <= 9:
                user = forms.cleaned_data["user"]
                EventMember.objects.create(event=event, user=user)
                return redirect("calendarapp:calendar")
            else:
                print("--------------User limit exceed!-----------------")
    context = {"form": forms}
    return render(request, "add_member.html", context)


class EventMemberDeleteView(generic.DeleteView):
    model = EventMember
    template_name = "event_delete.html"
    success_url = reverse_lazy("calendarapp:calendar")


class CalendarViewNew(LoginRequiredMixin, generic.View):
    login_url = "login"
    template_name = "calendarapp/calendar.html"
    form_class = EventForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        events = Event.objects.get_all_events(user=request.user)
        events_month = Event.objects.get_running_events(user=request.user)
        event_list = []
        # start: '2020-09-16T16:00:00'
        for event in events:
            event_list.append(
                {
                    "title": event.title,
                    "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),

                }
            )
        context = {"form": forms, "events": event_list,
                   "events_month": events_month}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.save()
            return redirect("calendarapp:calendar")
        context = {"form": forms}
        return render(request, self.template_name, context)
