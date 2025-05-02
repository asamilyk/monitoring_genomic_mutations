from django import forms

TYPES_OF_SEARCH = (
    (1, "По координатам"),
    (2, "По RS id"),
    (3, "По гену"),
    (4, "По болезни")
)


class GettingDataForm(forms.Form):
    search_type = forms.ChoiceField(choices=TYPES_OF_SEARCH)
    gene = forms.CharField()


class GenomicSearchForm(forms.Form):
    SEARCH_TYPES = [
        ('pos', 'Position'),
        ('gene_name', 'Gene Name'),
        ('gene_id', 'Gene ID'),
        ('disease_code', 'Disease Code'),
    ]
    
    search_type = forms.ChoiceField(choices=SEARCH_TYPES, required=True, label='Search by')
    search_term = forms.CharField(max_length=255, required=True, label='Search term')
    
    # Дополнительные поля для расширенного поиска
    chrom = forms.CharField(max_length=10, required=False, label='Chromosome')
    min_qual = forms.DecimalField(max_digits=5, decimal_places=1, required=False, label='Min Quality')
    annotation = forms.CharField(max_length=255, required=False, label='Annotation')
