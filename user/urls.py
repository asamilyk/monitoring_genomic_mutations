from django.urls import path
from . import views

app_name = 'user' 

urlpatterns = [
    path('filter-history/', views.filter_history, name='filter_history'),
    path('save-filter/', views.save_filter, name='save_filter'),
    path('delete-filter/<int:filter_id>/', views.delete_filter, name='delete_filter'),
]