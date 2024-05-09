from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload_csv_file/", views.upload_csv_file, name="upload_csv_file"),
    path("events/", views.create_event, name="create_event"),
    path("events/<int:event_id>/", views.event_detail, name="event_detail"),
    path("events/<int:event_id>/delete/", views.delete_event, name="delete_event"),
    path("events/<int:event_id>/edit/", views.edit_event, name="edit_event"),
    path("events/<int:event_id>/attendees/", views.email_attendees, name="email_attendees"),
]