from django.views.generic import ListView, CreateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import IntegrityError
from .models import Appointment
from .forms import AppointmentForm


class MyAppointmentsView(LoginRequiredMixin, ListView):
    """Мои записи с фильтрацией"""
    model = Appointment
    template_name = 'appointments/my.html'
    context_object_name = 'appointments'
    paginate_by = 10

    def get_queryset(self):
        queryset = Appointment.objects.filter(
            user=self.request.user
        ).select_related('doctor', 'service', 'doctor__specialization')

        # Фильтр по статусу
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # Фильтр по дате
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)

        # Сортировка
        sort = self.request.GET.get('sort')
        if sort == 'date_asc':
            queryset = queryset.order_by('date', 'time')
        elif sort == 'date_desc':
            queryset = queryset.order_by('-date', '-time')
        else:
            queryset = queryset.order_by('-date', '-time')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['current_filters'] = {
            'status': self.request.GET.get('status', ''),
            'date_from': self.request.GET.get('date_from', ''),
            'date_to': self.request.GET.get('date_to', ''),
            'sort': self.request.GET.get('sort', ''),
        }

        context['status_choices'] = Appointment.Status.choices

        return context


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    """Создание записи"""
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/create.html'
    success_url = reverse_lazy('appointments:my')

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            response = super().form_valid(form)
            messages.success(self.request, 'Вы записаны на приём!')
            return response
        except IntegrityError:
            messages.error(self.request, 'Это время уже занято.')
            return self.form_invalid(form)


class AppointmentDetailView(LoginRequiredMixin, DetailView):
    """Детали записи"""
    model = Appointment
    template_name = 'appointments/detail.html'
    context_object_name = 'appointment'

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)


class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    """Отмена записи"""
    model = Appointment
    template_name = 'appointments/delete.html'
    success_url = reverse_lazy('appointments:my')

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Запись отменена')
        return super().form_valid(form)