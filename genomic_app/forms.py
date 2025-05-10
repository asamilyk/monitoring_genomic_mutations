from django import forms
from .models import DataVcf

class GenomicFilterForm(forms.Form):
    COMPARISON_CHOICES = [
        ('', 'Выберите оператор'),
        ('eq', '='),
        ('gt', '>'),
        ('lt', '<'),
        ('gte', '>='),
        ('lte', '<='),
    ]
    

    def __init__(self, *args, **kwargs):
        super(GenomicFilterForm, self).__init__(*args, **kwargs)
        
        chromosome_choices = [('', 'Все хромосомы')]
        chromosomes = DataVcf.objects.values_list('chrom', flat=True).distinct().order_by('chrom')[:500]
        chromosome_choices.extend([(c, c) for c in chromosomes if c])
        
        disease_choices = [('', 'Все коды заболеваний')]
        diseases = DataVcf.objects.values_list('disease_code', flat=True).distinct().order_by('disease_code')[:500]
        disease_choices.extend([(d, d) for d in diseases if d])
        
        gene_name_choices = [('', 'Все гены')]
        gene_names = DataVcf.objects.values_list('gene_name', flat=True).distinct().order_by('gene_name')[:500]
        gene_name_choices.extend([(g, g) for g in gene_names if g])
        
        annotation_choices = [('', 'Все аннотации')]
        annotations = DataVcf.objects.values_list('annotation', flat=True).distinct().order_by('annotation')[:500]
        annotation_choices.extend([(a, a) for a in annotations if a])
        
        self.fields['chrom'] = forms.ChoiceField(
            label='Хромосома',
            choices=chromosome_choices,
            required=False
        )
        
        self.fields['disease_code'] = forms.ChoiceField(
            label='Код заболевания',
            choices=disease_choices,
            required=False
        )
        
        self.fields['gene_name'] = forms.ChoiceField(
            label='Имя гена',
            choices=gene_name_choices,
            required=False
        )
        
        self.fields['annotation'] = forms.ChoiceField(
            label='Аннотация',
            choices=annotation_choices,
            required=False
        )
        
        self.fields['qual_op'] = forms.ChoiceField(
            label='Qual оператор',
            choices=self.COMPARISON_CHOICES,
            required=False
        )
        
        self.fields['qual_value'] = forms.DecimalField(
            label='Qual значение',
            required=False,
            widget=forms.NumberInput(attrs={'step': '0.1', 'placeholder': 'Введите значение'}),
            max_digits=19,
            decimal_places=10
        )
