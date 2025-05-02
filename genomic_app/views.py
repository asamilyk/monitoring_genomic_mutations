from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from .models import DataVcf
from .tables import DataVcfTable
from .filters import DataVcfFilter

class DataVcfTableView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = DataVcf
    table_class = DataVcfTable
    template_name = 'genomic_app/data_table.html'
    filterset_class = DataVcfFilter
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related()
        
        return queryset[:100]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        filtered_count = self.filterset.qs.count()
        context['total_records'] = min(filtered_count, 100)
        context['limited_view'] = True
        
        return context
