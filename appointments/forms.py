from django import forms
from django.utils import timezone
from .models import Appointment, ContactRequest
from doctors.models import Doctor, TimeSlot
from services.models import Service


class AppointmentForm(forms.ModelForm):
    """Форма записи на приём с выбором слота"""

    time_slot = forms.ModelChoiceField(
        queryset=TimeSlot.objects.none(),
        widget=forms.HiddenInput(),
        required=False,
        label='Время'
    )

    class Meta:
        model = Appointment
        fields = ['doctor', 'service', 'date', 'comment']
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'service': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.filter(is_active=True)
        self.fields['service'].queryset = Service.objects.filter(is_active=True)
        self.fields['service'].required = False
        self.fields['date'].required = True
        self.fields['time_slot'].queryset = TimeSlot.objects.filter(is_available=True)

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        date = cleaned_data.get('date')
        time_slot = cleaned_data.get('time_slot')

        # ✅ Проверка: дата не в прошлом
        if date:
            today = timezone.now().date()
            if date < today:
                raise forms.ValidationError('Нельзя записаться на прошедшую дату.')

        # ✅ Проверка: слот выбран
        if doctor and date and not time_slot:
            raise forms.ValidationError('Пожалуйста, выберите время приёма.')

        # ✅ Проверка: слот свободен
        if time_slot:
            if time_slot.is_booked():
                raise forms.ValidationError(
                    'Это время уже занято. Выберите другое время.'
                )

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        time_slot = self.cleaned_data.get('time_slot')

        if time_slot:
            instance.date = time_slot.date
            instance.time = time_slot.time

        if commit:
            instance.save()
        return instance


class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
