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

        select_attrs = {
            'class': 'form-select select2-field',
            'data-placeholder': 'Начните вводить для поиска'
        }
        
        chromosome_choices = [('', 'Не выбрано')]
        chromosomes = DataVcf.objects.values_list('chrom', flat=True).distinct().order_by('chrom')
        chromosome_choices.extend([(c, c) for c in chromosomes if c])
        
        disease_choices = [('', 'Не выбрано')]
        diseases = DataVcf.objects.values_list('disease_code', flat=True).distinct().order_by('disease_code')
        disease_choices.extend([(d, d) for d in diseases if d])
        
        gene_name_choices = [('', 'Не выбрано')]
        gene_names = DataVcf.objects.values_list('gene_name', flat=True).distinct().order_by('gene_name')
        gene_name_choices.extend([(g, g) for g in gene_names if g])
        
        annotation_choices = [('', 'Не выбрано')]
        annotations = DataVcf.objects.values_list('annotation', flat=True).distinct().order_by('annotation')
        annotation_choices.extend([(a, a) for a in annotations if a])
        
        gene_id_choices = [('', 'Не выбрано')]
        gene_ids = DataVcf.objects.values_list('gene_id', flat=True).distinct().order_by('gene_id')
        gene_id_choices.extend([(g, g) for g in gene_ids if g])
        
        id_choices = [('', 'Не выбрано')]
        ids = DataVcf.objects.values_list('id', flat=True).distinct().order_by('id')
        id_choices.extend([(i, i) for i in ids if i])
        
        orig_id_choices = [('', 'Не выбрано')]
        orig_ids = DataVcf.objects.values_list('orig_id', flat=True).distinct().order_by('orig_id')
        orig_id_choices.extend([(o, o) for o in orig_ids if o])
        
        feature_type_choices = [('', 'Не выбрано')]
        feature_types = DataVcf.objects.values_list('feature_type', flat=True).distinct().order_by('feature_type')
        feature_type_choices.extend([(f, f) for f in feature_types if f])
        
        transcript_biotype_choices = [('', 'Не выбрано')]
        transcript_biotypes = DataVcf.objects.values_list('transcript_biotype', flat=True).distinct().order_by('transcript_biotype')
        transcript_biotype_choices.extend([(t, t) for t in transcript_biotypes if t])
        
        self.fields['chrom'] = forms.ChoiceField(
            label='Хромосома',
            choices=chromosome_choices,
            required=False,
            widget=forms.Select(attrs=select_attrs)
        )
        
        self.fields['disease_code'] = forms.ChoiceField(
            label='Код заболевания',
            choices=disease_choices,
            required=False,
            widget=forms.Select(attrs=select_attrs)
        )
        
        self.fields['gene_name'] = forms.ChoiceField(
            label='Имя гена',
            choices=gene_name_choices,
            required=False,
            widget=forms.Select(attrs=select_attrs)
        )
        
        self.fields['annotation'] = forms.ChoiceField(
            label='Аннотация',
            choices=annotation_choices,
            required=False,
            widget=forms.Select(attrs=select_attrs)
        )
        
        self.fields['gene_id'] = forms.ChoiceField(
            label='Gene ID',
            choices=gene_id_choices,
            required=False,
            widget=forms.Select(attrs=select_attrs)
        )
        
        self.fields['id'] = forms.ChoiceField(
            label='ID',
            choices=id_choices,
            required=False,
            widget=forms.Select(attrs=select_attrs)
        )
        
        self.fields['orig_id'] = forms.ChoiceField(
            label='Orig ID',
            choices=orig_id_choices,
            required=False,
            widget=forms.Select(attrs=select_attrs)
        )
        
        self.fields['feature_type'] = forms.ChoiceField(
            label='Feature Type',
            choices=feature_type_choices,
            required=False,
            widget=forms.Select(attrs=select_attrs)
        )
        
        self.fields['transcript_biotype'] = forms.ChoiceField(
            label='Transcript Biotype',
            choices=transcript_biotype_choices,
            required=False,
            widget=forms.Select(attrs=select_attrs)
        )
        
        self.fields['qual_op'] = forms.ChoiceField(
            label='Qual оператор',
            choices=self.COMPARISON_CHOICES,
            required=False,
            widget=forms.Select(attrs={'class': 'form-select'})
        )
        
        self.fields['qual_value'] = forms.DecimalField(
            label='Qual значение',
            required=False,
            widget=forms.NumberInput(attrs={
                'step': '0.1', 
                'placeholder': 'Введите значение',
                'class': 'form-control'
            }),
            max_digits=19,
            decimal_places=10
        )
