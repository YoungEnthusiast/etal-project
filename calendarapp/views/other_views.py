# cal/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
import calendar
from account.filters import InitiatedAllEventsFilter
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from account.models import Collab
from calendarapp.models import EventMember, Event
from calendarapp.utils import Calendar
from calendarapp.forms import EventForm, EventUpdateForm, AddMemberForm
from django.contrib import messages
from django.core.paginator import Paginator

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
    collab = Collab.objects.get(id=id1)
    collab_id = collab.id
    if collab.researcher == request.user:
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
                collab = collab,
                title=title,
                description=description,
                location=location,
                link=link,
                start_time=start_time,
                end_time=end_time,
                reminder=reminder,
            )
            messages.info(request, "The schedule has been added successfully")
            return redirect("calendarapp:schedules-initiated", id1)
        # else:
        #     messages.error(request, "Please review form input fields below")
        return render(request, "calendarapp/event.html", {"form": form, 'collab': collab, 'collab_id': collab_id})
    elif request.user in collab.collaborators.all():
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
                collab = collab,
                title=title,
                description=description,
                location=location,
                link=link,
                start_time=start_time,
                end_time=end_time,
                reminder=reminder,
            )
            messages.info(request, "The schedule has been added successfully")
            return redirect("calendarapp:schedules-initiated", id1)
        else:
            messages.error(request, "Please review form input fields below")
        return render(request, "calendarapp/event.html", {"form": form, 'collab': collab, 'collab_id': collab_id})
    else:
        return redirect('collab')

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

    def get(self, request, id1, *args, **kwargs):
        collab = Collab.objects.get(id=id1)
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
        context = {"form": forms, 'collab':collab, "events": event_list,
                   "events_month": events_month}
        return render(request, self.template_name, context)

    def post(self, request, id1, *args, **kwargs):
        collab = Collab.objects.get(id=id1)
        forms = self.form_class(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.collab = collab
            form.save()
            return redirect("calendarapp:schedules-initiated", id1)
        context = {"form": forms}

        return render(request, self.template_name, context)

@login_required
def showAllEventsInitiated(request, id1):
    collab = Collab.objects.get(id=id1)
    if collab.researcher == request.user:
        context = {}
        filtered_all_events = InitiatedAllEventsFilter(
            request.GET,
            queryset = Event.objects.filter(collab__id=id1)
        )
        context['filtered_all_events'] = filtered_all_events
        paginated_filtered_all_events = Paginator(filtered_all_events.qs, 99)
        page_number = request.GET.get('page')
        all_events_page_obj = paginated_filtered_all_events.get_page(page_number)
        context['all_events_page_obj'] = all_events_page_obj
        total_all_events = filtered_all_events.qs.count()
        context['total_all_events'] = total_all_events
        context['collab'] = collab

        return render(request, 'calendarapp/all_events.html', context)
    else:
        return redirect('collab')

@login_required
def selectEventInitiated(request, id1, id2, **kwargs):
    collab = Collab.objects.get(id=id1)
    if collab.researcher == request.user:
        event = Event.objects.get(id=id2)
        event.is_selected.add(request.user)
        event.save()
        return redirect('calendarapp:all-schedules-initiated', id1)
    else:
        return redirect('collab')

@login_required
def deselectEventInitiated(request, id1, id2, **kwargs):
    collab = Collab.objects.get(id=id1)
    if collab.researcher == request.user:
        event = Event.objects.get(id=id2)
        event.is_selected.remove(request.user)
        event.save()
        return redirect('calendarapp:all-schedules-initiated', id1)
    else:
        return redirect('collab')

@login_required
def deleteAllEventsInitiated(request, id1, **kwargs):
    collab = Collab.objects.get(id=id1)
    if collab.researcher == request.user:
        events = Event.objects.filter(is_selected=request.user, user=request.user, collab=collab)
        if events.count() >= 1:
            if request.method =="POST":
                for each in events:
                    each.delete()
                messages.info(request, "Deleted successfully")
                return redirect('calendarapp:all-schedules-initiated', id1)
        else:
            return redirect('calendarapp:all-schedules-initiated', id1)

        return render(request, 'calendarapp/events_confirm_delete_initiated.html', {'events':events, 'collab':collab})
    else:
        return redirect('collab')

@login_required
def showEventInitiated(request, id1, id2, **kwargs):
    collab = Collab.objects.get(id=id1)
    event = Event.objects.get(id=id2)
    if event.collab.researcher == request.user:
        context = {'collab': collab, 'event':event}

        return render(request, 'calendarapp/event_initiated.html', context)
    else:
        return redirect('collab')

@login_required
def updateEventInitiated(request, id1, id2):
    collab = Collab.objects.get(id=id1)
    event = Event.objects.get(id=id2)
    if event.collab.researcher == request.user:
        form = EventUpdateForm(instance=event)
        if request.method=='POST':
            form = EventUpdateForm(request.POST, instance=event)
            if form.is_valid():
                form.save()
                messages.info(request, "The shedule has been updated successfully")
                return redirect('calendarapp:all-schedules-initiated', id1)
    else:
        return redirect('collab')

    return render(request, 'calendarapp/update_event.html', {'form': form, 'collab':collab, 'event':event})

@login_required
def deleteEventInitiated(request, id1, id2):
    collab = Collab.objects.get(id=id1)
    event = Event.objects.get(id=id2)
    obj = get_object_or_404(Event, id=id2)
    if request.method =="POST":
        obj.delete()
        messages.info(request, "The event has been deleted successfully")
        return redirect('calendarapp:all-schedules-initiated', id1)
    return render(request, 'calendarapp/event_confirm_delete.html', {'collab':collab, 'event': event})

@login_required
def deleteEventInitiated(request, id1, id2):
    collab = Collab.objects.get(id=id1)
    event = Event.objects.get(id=id2)
    obj = get_object_or_404(Event, id=id2)
    if request.method =="POST":
        obj.delete()
        messages.info(request, "The event has been deleted successfully")
        return redirect('calendarapp:all-schedules-initiated', id1)
    return render(request, 'calendarapp/event_confirm_delete.html', {'collab':collab, 'event': event})



@login_required
def showEventInitiated2(request, id1, id2, **kwargs):
    collab = Collab.objects.get(id=id1)
    event = Event.objects.get(id=id2)
    start_time = request.GET.get('startdate')
    if event.collab.researcher == request.user:
        context = {'collab': collab, 'event':event}

        return render(request, 'calendarapp/event_initiated.html', context)
    else:
        return redirect('collab')
