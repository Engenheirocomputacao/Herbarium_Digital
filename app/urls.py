
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from fitoterapico.views import FitoterapicoListView, NovoFitoterapicoCreateView, FitoterapicoDetailView, FitoterapicoUpdateView, FitoterapicoDeleteView
from contas.views import registro_view, login_view, logout_view
from django.views.generic import RedirectView
from app.views import sobre_view, contato_view, acessibilidade_view, termos_view, dashboard_view



urlpatterns = [
    path('admin/', admin.site.urls),
    path('registro/',registro_view, name='registro'),
    path('login/',login_view, name='login'),
    path('logout/',logout_view, name='logout'),
    path('fitoterapico/', FitoterapicoListView.as_view(), name='fitoterapico_list'),
    path('novo_fitoterapico/', NovoFitoterapicoCreateView.as_view(), name='novo_fitoterapico'),
    path('fitoterapico/<int:pk>/', FitoterapicoDetailView.as_view(), name='fitoterapico_detail'),
    path('fitoterapico/<int:pk>/update/', FitoterapicoUpdateView.as_view(), name='fitoterapico_update'),
    path('fitoterapico/<int:pk>/delete/', FitoterapicoDeleteView.as_view(), name='fitoterapico_delete'),
    path('', RedirectView.as_view(url='/fitoterapico/', permanent=True), name='home'),
    path('sobre/', sobre_view, name='sobre'),
    path('contato/', contato_view, name='contato'),
    path('acessibilidade/', acessibilidade_view, name='acessibilidade'),
    path('termos/', termos_view, name='termos'),
    path('dashboard/', dashboard_view, name='dashboard'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


