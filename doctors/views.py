from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Doctor, Specialization


class DoctorListView(ListView):
    """Список врачей с поиском и фильтрацией"""
    model = Doctor
    template_name = 'doctors/list.html'
    context_object_name = 'doctors'
    paginate_by = 12

    def get_queryset(self):
        queryset = Doctor.objects.select_related('specialization').filter(is_active=True)

        # Поиск по имени
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(middle_name__icontains=search) |
                Q(bio__icontains=search)
            )

        # Фильтр по специализации
        specialization_slug = self.kwargs.get('specialization_slug')
        if specialization_slug:
            queryset = queryset.filter(specialization__slug=specialization_slug)

        # Фильтр по опыту
        min_experience = self.request.GET.get('min_experience')
        if min_experience:
            queryset = queryset.filter(experience__gte=min_experience)

        # ✅ Сортировка
        sort = self.request.GET.get('sort')
        if sort == 'experience':
            queryset = queryset.order_by('-experience')
        elif sort == 'name':
            queryset = queryset.order_by('last_name', 'first_name')
        else:
            queryset = queryset.order_by('last_name', 'first_name')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['specializations'] = Specialization.objects.all()

        context['current_filters'] = {
            'search': self.request.GET.get('search', ''),
            'min_experience': self.request.GET.get('min_experience', ''),
            'sort': self.request.GET.get('sort', ''),
        }
        return context


class DoctorDetailView(DetailView):
    """Детализация по врачам"""
    model = Doctor
    template_name = 'doctors/detail.html'
    context_object_name = 'doctor'
