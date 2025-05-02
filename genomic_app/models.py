# models.py
from django.db import models

class LimitedDataManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()[:100000]

class DataVcf(models.Model):
    id = models.IntegerField(primary_key=True)
    orig_id = models.CharField(max_length=255, null=True, blank=True)
    chrom = models.TextField(null=True, blank=True)
    pos = models.IntegerField(null=True, blank=True)
    ref = models.CharField(max_length=255, null=True, blank=True)
    alt = models.CharField(max_length=255, null=True, blank=True)
    qual = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    annotation = models.CharField(max_length=255, null=True, blank=True)
    gene_id = models.CharField(max_length=255, null=True, blank=True)
    gene_name = models.CharField(max_length=255, null=True, blank=True)
    feature_id = models.CharField(max_length=255, null=True, blank=True)
    feature_type = models.CharField(max_length=255, null=True, blank=True)
    transcript_biotype = models.CharField(max_length=255, null=True, blank=True)
    hgvs_c = models.CharField(max_length=255, null=True, blank=True)
    disease_code = models.CharField(max_length=10, null=True, blank=True)

    objects = models.Manager()
    
    limited = LimitedDataManager()

    class Meta:
        managed = False
        db_table = 'crd_dmt\".\"data_vcf'
        app_label = 'genomic_app'
        verbose_name = 'Genomic Data'
        verbose_name_plural = 'Genomic Data'
        default_manager_name = 'limited'
    
    def __str__(self):
        return f"{self.gene_name} - {self.pos} - {self.hgvs_c}"
