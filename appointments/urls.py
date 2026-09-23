from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.MyAppointmentsView.as_view(), name='my'),
    path('create/', views.AppointmentCreateView.as_view(), name='create'),
    path('<int:pk>/', views.AppointmentDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', views.AppointmentDeleteView.as_view(), name='delete'),
    path('api/available-slots/', views.AvailableSlotsView.as_view(), name='available_slots'),
]
