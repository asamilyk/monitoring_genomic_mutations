from django.db import models

class DataVcf(models.Model):
    row_id = models.AutoField(primary_key=True)
    id = models.IntegerField(blank=True, null=True)
    orig_id = models.CharField(max_length=255, blank=True, null=True)
    chrom = models.TextField(blank=True, null=True)
    pos = models.IntegerField(blank=True, null=True)
    ref = models.CharField(max_length=255, blank=True, null=True)
    alt = models.CharField(max_length=255, blank=True, null=True)
    qual = models.DecimalField(max_digits=19, decimal_places=10, blank=True, null=True)
    annotation = models.CharField(max_length=255, blank=True, null=True)
    gene_id = models.CharField(max_length=255, blank=True, null=True)
    gene_name = models.CharField(max_length=255, blank=True, null=True)
    feature_id = models.CharField(max_length=255, blank=True, null=True)
    feature_type = models.CharField(max_length=255, blank=True, null=True)
    transcript_biotype = models.CharField(max_length=255, blank=True, null=True)
    hgvs_c = models.CharField(max_length=255, blank=True, null=True)
    disease_code = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'crd_dmt\".\"data_vcf_new_2'
        app_label = 'genomic_app'  
        
    def __str__(self):
        return f"{self.gene_name} - {self.chrom}:{self.pos} {self.ref}>{self.alt}"
