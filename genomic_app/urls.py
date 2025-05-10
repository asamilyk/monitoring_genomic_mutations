from django.urls import path
from . import views

app_name = 'genomic_app'

urlpatterns = [
    path('', views.data_table, name='data_table'),
    path('data/', views.data_table, name='data_table'),
]
