from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView, ListView, CreateView
from .models import CompanyInfo, Advantage
from services.models import Service
from appointments.models import ContactRequest


class HomeView(TemplateView):
    """Главная страница"""
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = CompanyInfo.objects.first()
        context['advantages'] = Advantage.objects.all()
        context['services'] = Service.objects.filter(is_active=True)[:6]
        return context


class AboutView(TemplateView):
    """Страница О компании"""
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = CompanyInfo.objects.first()
        return context


class ContactsView(TemplateView):
    """Страница Контакты"""
    template_name = 'main/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = CompanyInfo.objects.first()
        return context

    def post(self, request, *args, **kwargs):
        """Обработка формы обратной связи"""
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        if name and email and message:
            ContactRequest.objects.create(
                name=name,
                email=email,
                phone=phone,
                message=message
            )
            messages.success(request, 'Спасибо! Мы свяжемся с вами в ближайшее время.')
        else:
            messages.error(request, 'Пожалуйста, заполните все обязательные поля.')

        return redirect('main:contacts')
