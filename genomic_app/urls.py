from django.urls import path
from . import views

app_name = 'genomic_app'

urlpatterns = [
    path('', views.DataVcfTableView.as_view(), name='data_table'),
    path('data/', views.DataVcfTableView.as_view(), name='data_table'),
]