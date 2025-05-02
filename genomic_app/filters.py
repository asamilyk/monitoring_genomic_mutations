import django_filters
from django import forms
from .models import DataVcf

class DataVcfFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(label='ID')
    
    pos = django_filters.NumberFilter(label='Position')
    pos_min = django_filters.NumberFilter(field_name='pos', lookup_expr='gte', label='Position ≥')
    pos_max = django_filters.NumberFilter(field_name='pos', lookup_expr='lte', label='Position ≤')
    
    CHROM_CHOICES = [
        ('', 'All'),
        ('chr1', 'chr1'), ('chr2', 'chr2'), ('chr3', 'chr3'), ('chr4', 'chr4'),
        ('chr5', 'chr5'), ('chr6', 'chr6'), ('chr7', 'chr7'), ('chr8', 'chr8'),
        ('chr9', 'chr9'), ('chr10', 'chr10'), ('chr11', 'chr11'), ('chr12', 'chr12'),
        ('chr13', 'chr13'), ('chr14', 'chr14'), ('chr15', 'chr15'), ('chr16', 'chr16'),
        ('chr17', 'chr17'), ('chr18', 'chr18'), ('chr19', 'chr19'), ('chr20', 'chr20'),
        ('chr21', 'chr21'), ('chr22', 'chr22'), ('chrX', 'chrX'), ('chrY', 'chrY'),
        ('chrM', 'chrM'),
    ]
    chrom = django_filters.ChoiceFilter(choices=CHROM_CHOICES, label='Chromosome')
    
    gene_name = django_filters.CharFilter(lookup_expr='icontains', label='Gene Name')
    gene_id = django_filters.CharFilter(lookup_expr='icontains', label='Gene ID')

    qual_min = django_filters.NumberFilter(field_name='qual', lookup_expr='gte', label='Quality ≥')

    disease_code = django_filters.CharFilter(lookup_expr='icontains', label='Disease Code')
    
    class Meta:
        model = DataVcf
        fields = [
            'id', 'chrom', 'pos', 'ref', 'alt', 'gene_name', 
            'gene_id', 'disease_code'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for name, field in self.filters.items():
            if isinstance(field, django_filters.CharFilter):
                field.field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': f'Search {field.label}'
                })
            elif isinstance(field, django_filters.NumberFilter):
                field.field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': field.label
                })
            elif isinstance(field, django_filters.ChoiceFilter):
                field.field.widget.attrs.update({
                    'class': 'form-control'
                })
