from django.views.generic import ListView, DetailView
from django.db.models import Q, Min, Max
from .models import Service, ServiceCategory


class ServiceListView(ListView):
    """Список услуг с поиском и фильтрацией"""
    model = Service
    template_name = 'services/list.html'
    context_object_name = 'services'
    paginate_by = 9

    def get_queryset(self):
        queryset = Service.objects.select_related('category').filter(is_active=True)

        # ✅ Поиск по названию и описанию
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(short_description__icontains=search) |
                Q(full_description__icontains=search)
            )

        # ✅ Фильтр по категории
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # ✅ Фильтр по цене
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # ✅ Сортировка
        sort = self.request.GET.get('sort')
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort == 'name':
            queryset = queryset.order_by('name')
        else:
            queryset = queryset.order_by('category', 'name')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ✅ Категории для фильтра
        context['categories'] = ServiceCategory.objects.all()

        # ✅ Текущие фильтры (для сохранения в пагинации)
        context['current_filters'] = {
            'search': self.request.GET.get('search', ''),
            'min_price': self.request.GET.get('min_price', ''),
            'max_price': self.request.GET.get('max_price', ''),
            'sort': self.request.GET.get('sort', ''),
        }

        # ✅ Диапазон цен
        price_range = Service.objects.filter(is_active=True).aggregate(
            min_price=Min('price'),
            max_price=Max('price')
        )
        context['price_range'] = price_range

        return context


class ServiceDetailView(DetailView):
    """Детали услуги"""
    model = Service
    template_name = 'services/detail.html'
    context_object_name = 'service'
    slug_field = 'slug'
