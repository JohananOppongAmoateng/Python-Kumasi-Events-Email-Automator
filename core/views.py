from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from .forms import UploadCSVFileForm, EventForm
from .models import Attendee, Event
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string

# Create your views here.
import csv


def create_attendee_from_csv(csv_file, request):
    csv_file = csv_file.read().decode("utf-8").splitlines()
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        _, created = Attendee.objects.get_or_create(
            name=row["Name"],
            email=row["Email"],
            phone=row["Phone"],
            user_id=request.user,
        )



@login_required(login_url="/accounts/login/")
def index(request):
    events = Event.objects.filter(user_id=request.user)
    return render(request, "core/index.html", {"events": events})


@login_required(login_url="/accounts/login/")
def upload_csv_file(request):
    if request.method == "POST":
        form = UploadCSVFileForm(request.POST,request.FILES)
        if form.is_valid():
            csv_file = request.FILES["csv"]
            print("Valid file uploaded")
            # print(csv_file)
            print(csv_file)
            create_attendee_from_csv(csv_file, request)
            return redirect("index")
    else:
        form = UploadCSVFileForm()
    return render(request, "core/upload_csv_file.html", {"form": form})


def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user_id = request.user
            event.save()
            return redirect("index")
    else:
        form = EventForm()
    return render(request, "core/create_event.html", {"form": form})


def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, user_id=request.user)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            return redirect("event_detail", event_id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, "core/edit_event.html", {"form": form, "event": event})


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id, user_id=request.user)
    return render(request, "core/event_detail.html", {"event": event})


def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, user_id=request.user)
    event.delete()
    return redirect("index")


@login_required(login_url="/accounts/login/")
def email_attendees(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    attendees = get_list_or_404(Attendee, user_id=request.user)
    user = request.user

    subject = f"Invitation to {event.title} event by {request.user.username}"
    messages = []
    for attendee in attendees:
        # Prepare a list of attendee names
        attendee_name = attendee.name

        # Pass attendee name to the template context
        context = {"event": event, "attendee_name": attendee_name, "user": user}

        message = render_to_string("core/email_attendees.txt", context)

        messages.append((subject, message, user.email, [attendee.email]))

    # Send all emails at once
    send_mass_mail(messages)

    return render(
        request,
        "core/event_detail.html",
        {"event": event, "message": "Emails sent successfully!"},
    )
