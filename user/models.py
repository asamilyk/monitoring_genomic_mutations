from django.db import models
from django.contrib.auth.models import User
import json

class FilterHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='filter_history')
    filter_name = models.CharField(max_length=255, blank=True, null=True)
    filter_params = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'История фильтров'
        verbose_name_plural = 'История фильтров'
    
    def __str__(self):
        return f"{self.user.username} - {self.filter_name or 'Безымянный фильтр'} ({self.created_at.strftime('%d.%m.%Y %H:%M')})"
    
    def get_filter_params(self):
        try:
            return json.loads(self.filter_params)
        except json.JSONDecodeError:
            return {}
    
    def get_filter_url(self):
        from django.urls import reverse
        from urllib.parse import urlencode
        
        base_url = reverse('genomic_app:data_table')
        params = self.get_filter_params()
        
        for key in ['last_row_id', 'direction', 'page']:
            if key in params:
                del params[key]
        
        if params:
            return f"{base_url}?{urlencode(params)}"
        return base_url
    
    def get_filter_description(self):
        params = self.get_filter_params()
        descriptions = []
        
        field_names = {
            'chrom': 'Хромосома',
            'pos': 'Позиция',
            'ref': 'Ref',
            'alt': 'Alt',
            'gene_name': 'Имя гена',
            'gene_id': 'Gene ID',
            'feature_id': 'Feature ID',
            'feature_type': 'Feature Type',
            'transcript_biotype': 'Transcript Biotype',
            'hgvs_c': 'HGVS C',
            'disease_code': 'Код заболевания',
            'annotation': 'Аннотация',
            'id': 'ID',
            'orig_id': 'Orig ID',
            'variant_combo': 'Вариант'
        }
        
        for key, value in params.items():
            if key == 'qual_op' and 'qual_value' in params:
                op_map = {'eq': '=', 'gt': '>', 'lt': '<', 'gte': '>=', 'lte': '<='}
                op = op_map.get(value, value)
                descriptions.append(f"Qual {op} {params['qual_value']}")
            elif key != 'qual_value' and value and key in field_names:
                descriptions.append(f"{field_names.get(key, key)}: {value}")
        
        return ", ".join(descriptions) or "Без фильтров"
