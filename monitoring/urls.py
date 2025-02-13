from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_data_form, name='get_data'),
    path('display_data/', views.display_last, name='display_last'),
    path('/<int:search_type>/<str:gene>', views.display_result, name="display_result")
]
