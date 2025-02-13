from django.urls import path
from .views import UpdatedLoginView

urlpatterns = [
    path('login/', UpdatedLoginView.as_view(), name='login'),  # Заменяем стандартный login
]