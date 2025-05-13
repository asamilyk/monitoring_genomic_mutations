from django.shortcuts import render
from django.db.models import Q
from .models import DataVcf
from .forms import GenomicFilterForm
from django.contrib.auth.decorators import login_required
import csv
from django.http import HttpResponse
import xlsxwriter
from io import BytesIO

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
        gene_id = form.cleaned_data.get('gene_id')
        id_value = form.cleaned_data.get('id')
        orig_id = form.cleaned_data.get('orig_id')
        feature_type = form.cleaned_data.get('feature_type')
        transcript_biotype = form.cleaned_data.get('transcript_biotype')
        qual_op = form.cleaned_data.get('qual_op')
        qual_value = form.cleaned_data.get('qual_value')
        
        pos = form.cleaned_data.get('pos')
        ref = form.cleaned_data.get('ref')
        alt = form.cleaned_data.get('alt')
        feature_id = form.cleaned_data.get('feature_id')
        hgvs_c = form.cleaned_data.get('hgvs_c')
        
        variant_combo = form.cleaned_data.get('variant_combo')
        
        if chrom:
            base_query = base_query.filter(chrom=chrom)
        if disease_code:
            base_query = base_query.filter(disease_code=disease_code)
        if gene_name:
            base_query = base_query.filter(gene_name=gene_name)
        if annotation:
            base_query = base_query.filter(annotation=annotation)
        if gene_id:
            base_query = base_query.filter(gene_id=gene_id)
        if id_value:
            base_query = base_query.filter(id=id_value)
        if orig_id:
            base_query = base_query.filter(orig_id=orig_id)
        if feature_type:
            base_query = base_query.filter(feature_type=feature_type)
        if transcript_biotype:
            base_query = base_query.filter(transcript_biotype=transcript_biotype)
        
        if pos:
            base_query = base_query.filter(pos=pos)
        if ref:
            base_query = base_query.filter(ref=ref)
        if alt:
            base_query = base_query.filter(alt=alt)
        if feature_id:
            base_query = base_query.filter(feature_id=feature_id)
        if hgvs_c:
            base_query = base_query.filter(hgvs_c=hgvs_c)
        
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
        
        if variant_combo:
            parts = variant_combo.split('|')
            if len(parts) == 4:
                chrom, pos_str, ref, alt = parts
                try:
                    pos = int(pos_str)
                    base_query = base_query.filter(
                        chrom=chrom,
                        pos=pos,
                        ref=ref,
                        alt=alt
                    )
                except ValueError:
                    pass
    
    export_format = request.GET.get('export')
    if export_format:
        return export_data(request, base_query, export_format)
        
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
        'has_active_filters': bool(any(request.GET.get(key) for key in request.GET if key not in ['page', 'last_row_id', 'direction', 'export'])),
    }
    
    return render(request, 'genomic_app/data_table.html', context)


def export_data(request, queryset, format):

    field_names = [
        'row_id', 'id', 'orig_id', 'chrom', 'pos', 'ref', 'alt', 'qual',
        'annotation', 'gene_id', 'gene_name', 'feature_id', 'feature_type',
        'transcript_biotype', 'hgvs_c', 'disease_code'
    ]
    
    headers = [
        'Row ID', 'ID', 'Orig ID', 'Хромосома', 'Позиция', 'Ref', 'Alt', 'Qual',
        'Аннотация', 'Gene ID', 'Gene Name', 'Feature ID', 'Feature Type',
        'Transcript Biotype', 'HGVS C', 'Код заболевания'
    ]
    
    MAX_EXPORT_RECORDS = 10000  
    queryset = queryset.order_by('row_id')[:MAX_EXPORT_RECORDS]
    
    filename = f"genomic_data_export"
    
    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(headers)
        
        for record in queryset.iterator():
            writer.writerow([getattr(record, field) for field in field_names])
        
        return response
    
    elif format == 'excel':
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('Данные')
        
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#4F81BD',
            'color': 'white',
            'border': 1
        })
        
        cell_format = workbook.add_format({
            'border': 1
        })
        
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, header_format)

        for row_num, record in enumerate(queryset.iterator(), 1):
            for col_num, field in enumerate(field_names):
                value = getattr(record, field)
                worksheet.write(row_num, col_num, value, cell_format)

        for col_num, _ in enumerate(headers):
            worksheet.set_column(col_num, col_num, 15)
        
        workbook.close()
        
        output.seek(0)
        
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
        
        return response
    
    return HttpResponse("Invalid export format requested", status=400)
