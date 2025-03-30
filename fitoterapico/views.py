from django.urls import reverse_lazy
from fitoterapico.models import Fitoterapico
from fitoterapico.forms import FitoterapicoModelForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

    
class FitoterapicoListView(ListView):
    model = Fitoterapico
    template_name = 'fitoterapico.html'
    context_object_name = 'fitoterapico'
    paginate_by = 9

    def get_queryset(self):
        fitoterapico = super().get_queryset().order_by('nome')
        search = self.request.GET.get('search', '')
        tipo = self.request.GET.get('tipo', '')
        indicacao = self.request.GET.get('indicacao', '')

        if search:
            fitoterapico = fitoterapico.filter(nome__icontains=search)
        
        if tipo:
            fitoterapico = fitoterapico.filter(tipo__id=tipo)
            
        if indicacao:
            fitoterapico = fitoterapico.filter(indicacao__icontains=indicacao)

        return fitoterapico

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from fitoterapico.models import Tipo
        
        context['search'] = self.request.GET.get('search', '')
        context['tipo_selecionado'] = self.request.GET.get('tipo', '')
        context['indicacao'] = self.request.GET.get('indicacao', '')
        context['tipos'] = Tipo.objects.all()
        return context




@method_decorator(login_required(login_url='login'), name='dispatch')
class NovoFitoterapicoCreateView(CreateView):
    model = Fitoterapico
    form_class = FitoterapicoModelForm
    template_name = 'novo_fitoterapico.html'
    success_url = '/fitoterapico/'



class FitoterapicoDetailView(DetailView):
    model = Fitoterapico
    template_name = 'fitoterapico_detail.html'


@method_decorator(login_required(login_url='login'), name='dispatch')
class FitoterapicoUpdateView(UpdateView):
    model = Fitoterapico
    form_class = FitoterapicoModelForm
    template_name = 'fitoterapico_update.html'
    
    def get_success_url(self):
        return reverse_lazy('fitoterapico_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required(login_url='login'), name='dispatch')
class FitoterapicoDeleteView(DeleteView):
    model = Fitoterapico
    template_name = 'fitoterapico_delete.html'
    success_url = '/fitoterapico/'