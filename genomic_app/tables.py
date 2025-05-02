import django_tables2 as tables
from .models import DataVcf

class DataVcfTable(tables.Table):
    id = tables.Column(linkify=False)
    
    gene_name = tables.Column(attrs={"td": {"style": "font-weight: bold;"}})
    
    annotation = tables.Column(attrs={"td": {"title": lambda record: record.annotation}})
    
    hgvs_c = tables.Column(attrs={"td": {"style": "max-width: 150px; overflow: hidden; text-overflow: ellipsis;"}})
    
    class Meta:
        model = DataVcf
        template_name = "django_tables2/bootstrap4.html"
        fields = (
            'id', 'chrom', 'pos', 'ref', 'alt', 'qual', 'gene_name', 
            'gene_id', 'annotation', 'feature_id', 'feature_type', 
            'transcript_biotype', 'hgvs_c', 'disease_code'
        )
        attrs = {
            "class": "table table-striped table-hover table-sm",
            "thead": {"class": "thead-light"}
        }
        row_attrs = {
            "data-id": lambda record: record.pk
        }
