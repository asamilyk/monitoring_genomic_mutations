from django.shortcuts import render
from django.db.models import Q
from .models import DataVcf
from .forms import GenomicFilterForm

def data_table(request):
    form = GenomicFilterForm(request.GET or None)
    
    page_size = 100
    
    try:
        last_row_id = int(request.GET.get('last_row_id', 0)) or None
    except ValueError:
        last_row_id = None
    
    direction = request.GET.get('direction', 'next') 
    

    base_query = DataVcf.objects
    
    if form.is_valid():
        chrom = form.cleaned_data.get('chrom')
        disease_code = form.cleaned_data.get('disease_code')
        gene_name = form.cleaned_data.get('gene_name')
        annotation = form.cleaned_data.get('annotation')
        qual_op = form.cleaned_data.get('qual_op')
        qual_value = form.cleaned_data.get('qual_value')
        
        if chrom:
            base_query = base_query.filter(chrom=chrom)
        if disease_code:
            base_query = base_query.filter(disease_code=disease_code)
        if gene_name:
            base_query = base_query.filter(gene_name=gene_name)
        if annotation:
            base_query = base_query.filter(annotation=annotation)
        
        if qual_op and qual_value is not None:
            if qual_op == 'eq':
                base_query = base_query.filter(qual=qual_value)
            elif qual_op == 'gt':
                base_query = base_query.filter(qual__gt=qual_value)
            elif qual_op == 'lt':
                base_query = base_query.filter(qual__lt=qual_value)
            elif qual_op == 'gte':
                base_query = base_query.filter(qual__gte=qual_value)
            elif qual_op == 'lte':
                base_query = base_query.filter(qual__lte=qual_value)
    
    query = base_query
    
    is_first_page = last_row_id is None or (
        direction == 'prev' and 
        not base_query.filter(row_id__lt=last_row_id).exists()
    )
    
    if last_row_id and direction == 'next':
        query = query.filter(row_id__gt=last_row_id).order_by('row_id')
    elif last_row_id and direction == 'prev':
        query = query.filter(row_id__lt=last_row_id).order_by('-row_id')
    else:
        query = query.order_by('row_id')
        is_first_page = True

    records = list(query[:page_size + 1])
    
    if not records:
        context = {
            'form': form,
            'records': [],
            'has_next': False,
            'has_prev': False,
            'is_first_page': True,
            'total_count': DataVcf.objects.count(),
            'filtered_count': base_query.count(),
        }
        return render(request, 'genomic_app/data_table.html', context)

    has_next_by_count = len(records) > page_size
    if has_next_by_count:
        records = records[:page_size]  
    
    if direction == 'prev':
        records.reverse()
    
    first_record_row_id = records[0].row_id if records else None
    last_record_row_id = records[-1].row_id if records else None
    
    has_prev = False
    if first_record_row_id is not None:
        has_prev = base_query.filter(row_id__lt=first_record_row_id).exists()
    
    if is_first_page:
        has_prev = False

    has_next = False
    if last_record_row_id is not None:
        has_next = base_query.filter(row_id__gt=last_record_row_id).exists()
    else:
        has_next = False
    
    context = {
        'form': form,
        'records': records,
        'has_next': has_next,
        'has_prev': has_prev,
        'is_first_page': is_first_page,
        'first_record_row_id': first_record_row_id,
        'last_record_row_id': last_record_row_id,
        'total_count': DataVcf.objects.count(),
        'filtered_count': base_query.count(),
    }
    
    return render(request, 'genomic_app/data_table.html', context)
