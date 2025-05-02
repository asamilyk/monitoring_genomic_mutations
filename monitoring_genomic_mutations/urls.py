from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('genomic_data/', include('genomic_app.urls', namespace='genomic_app')),
    path('', login_required(RedirectView.as_view(url='/genomic_data/data/')), name='index'),
]
