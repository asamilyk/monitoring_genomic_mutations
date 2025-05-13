from django import forms
from .models import DataVcf

class GenomicFilterForm(forms.Form):
    
    chrom = forms.ChoiceField(
        label='Хромосома',
        choices=[('', 'Все хромосомы')],
        required=False
    )
    
    disease_code = forms.ChoiceField(
        label='Код заболевания',
        choices=[('', 'Все коды заболеваний')],
        required=False
    )
    
    gene_name = forms.ChoiceField(
        label='Имя гена',
        choices=[('', 'Все гены')],
        required=False
    )
    
    annotation = forms.ChoiceField(
        label='Аннотация',
        choices=[('', 'Все аннотации')],
        required=False
    )
    
    gene_id = forms.ChoiceField(
        label='Gene ID',
        choices=[('', 'Все Gene ID')],
        required=False
    )
    
    id = forms.ChoiceField(
        label='ID',
        choices=[('', 'Все ID')],
        required=False
    )
    
    orig_id = forms.ChoiceField(
        label='Orig ID',
        choices=[('', 'Все Orig ID')],
        required=False
    )
    
    feature_type = forms.ChoiceField(
        label='Feature Type',
        choices=[('', 'Все Feature Type')],
        required=False
    )
    
    transcript_biotype = forms.ChoiceField(
        label='Transcript Biotype',
        choices=[('', 'Все Transcript Biotype')],
        required=False
    )
    
    pos = forms.IntegerField(
        label='Позиция',
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Введите позицию'})
    )
    
    ref = forms.CharField(
        label='Ref',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Введите ref'})
    )
    
    alt = forms.CharField(
        label='Alt',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Введите alt'})
    )
    
    feature_id = forms.ChoiceField(
        label='Feature ID',
        choices=[('', 'Все Feature ID')],
        required=False
    )
    
    hgvs_c = forms.ChoiceField(
        label='HGVS C',
        choices=[('', 'Все HGVS C')],
        required=False
    )
    
    qual_op = forms.ChoiceField(
        label='Qual оператор',
    choices=[
        ('', 'Выберите оператор'),
        ('eq', '='),
        ('gt', '>'),
        ('lt', '<'),
        ('gte', '>='),
        ('lte', '<='),
    ],
    required=False,
    widget=forms.Select(attrs={'class': 'form-select'}))
    
    qual_value = forms.DecimalField(
        label='Qual значение',
        required=False,
        widget=forms.NumberInput(attrs={'step': '0.1', 'placeholder': 'Введите значение'}),
        max_digits=19,
        decimal_places=10
    )
    
    variant_combo = forms.ChoiceField(
        label='Вариант (chrom+pos+ref+alt)',
        required=False,
        choices=[('', 'Выберите вариант')]
    )
    
    def __init__(self, *args, **kwargs):
        super(GenomicFilterForm, self).__init__(*args, **kwargs)
        
        chromosome_choices = [('', 'Все хромосомы')]
        chromosomes = DataVcf.objects.values_list('chrom', flat=True).distinct().order_by('chrom')
        chromosome_choices.extend([(c, c) for c in chromosomes if c])
        self.fields['chrom'].choices = chromosome_choices
        
        disease_choices = [('', 'Все коды заболеваний')]
        diseases = DataVcf.objects.values_list('disease_code', flat=True).distinct().order_by('disease_code')
        disease_choices.extend([(d, d) for d in diseases if d])
        self.fields['disease_code'].choices = disease_choices
        
        gene_name_choices = [('', 'Все гены')]
        gene_names = DataVcf.objects.values_list('gene_name', flat=True).distinct().order_by('gene_name')[:500]
        gene_name_choices.extend([(g, g) for g in gene_names if g])
        self.fields['gene_name'].choices = gene_name_choices
        
        annotation_choices = [('', 'Все аннотации')]
        annotations = DataVcf.objects.values_list('annotation', flat=True).distinct().order_by('annotation')[:500]
        annotation_choices.extend([(a, a) for a in annotations if a])
        self.fields['annotation'].choices = annotation_choices
        
        gene_id_choices = [('', 'Все Gene ID')]
        gene_ids = DataVcf.objects.values_list('gene_id', flat=True).distinct().order_by('gene_id')[:500]
        gene_id_choices.extend([(g, g) for g in gene_ids if g])
        self.fields['gene_id'].choices = gene_id_choices
        
        id_choices = [('', 'Все ID')]
        ids = DataVcf.objects.values_list('id', flat=True).distinct().order_by('id')[:500]
        id_choices.extend([(i, i) for i in ids if i is not None])
        self.fields['id'].choices = id_choices
        
        orig_id_choices = [('', 'Все Orig ID')]
        orig_ids = DataVcf.objects.values_list('orig_id', flat=True).distinct().order_by('orig_id')[:500]
        orig_id_choices.extend([(o, o) for o in orig_ids if o])
        self.fields['orig_id'].choices = orig_id_choices
        
        feature_type_choices = [('', 'Все Feature Type')]
        feature_types = DataVcf.objects.values_list('feature_type', flat=True).distinct().order_by('feature_type')
        feature_type_choices.extend([(f, f) for f in feature_types if f])
        self.fields['feature_type'].choices = feature_type_choices
        
        transcript_biotype_choices = [('', 'Все Transcript Biotype')]
        transcript_biotypes = DataVcf.objects.values_list('transcript_biotype', flat=True).distinct().order_by('transcript_biotype')
        transcript_biotype_choices.extend([(t, t) for t in transcript_biotypes if t])
        self.fields['transcript_biotype'].choices = transcript_biotype_choices
        
        feature_id_choices = [('', 'Все Feature ID')]
        feature_ids = DataVcf.objects.values_list('feature_id', flat=True).distinct().order_by('feature_id')[:500]
        feature_id_choices.extend([(f, f) for f in feature_ids if f])
        self.fields['feature_id'].choices = feature_id_choices
        
        hgvs_c_choices = [('', 'Все HGVS C')]
        hgvs_cs = DataVcf.objects.values_list('hgvs_c', flat=True).distinct().order_by('hgvs_c')[:500]
        hgvs_c_choices.extend([(h, h) for h in hgvs_cs if h])
        self.fields['hgvs_c'].choices = hgvs_c_choices
        
        variant_choices = [('', 'Выберите вариант')]
        combos = DataVcf.objects.values('chrom', 'pos', 'ref', 'alt').distinct()
        
        for combo in combos:
            chrom = combo['chrom'] or ''
            pos = str(combo['pos']) if combo['pos'] is not None else ''
            ref = combo['ref'] or ''
            alt = combo['alt'] or ''
            
            if all([chrom, pos, ref, alt]): 
                display_value = f"{chrom}:{pos} {ref}>{alt}"
                value = f"{chrom}|{pos}|{ref}|{alt}"
                variant_choices.append((value, display_value))
        
        self.fields['variant_combo'].choices = variant_choices
