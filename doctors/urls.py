from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.DoctorListView.as_view(), name='list'),
    path('specialization/<slug:specialization_slug>/', views.DoctorListView.as_view(), name='specialization'),
    path('<int:pk>/', views.DoctorDetailView.as_view(), name='detail'),
]
