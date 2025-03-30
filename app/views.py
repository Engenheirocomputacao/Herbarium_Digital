from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from fitoterapico.models import Fitoterapico, FitoterapicoInventario
from django.db.models import Count, Avg, Sum
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta

def sobre_view(request):
    return render(request, 'paginas/sobre.html')

def contato_view(request):
    return render(request, 'paginas/contato.html')

def acessibilidade_view(request):
    return render(request, 'paginas/acessibilidade.html')

def termos_view(request):
    return render(request, 'paginas/termos.html')

@login_required(login_url='login')
def dashboard_view(request):
    # Dados para o gráfico de fitoterápicos por tipo
    tipos_data = Fitoterapico.objects.values('tipo__nome').annotate(count=Count('id'))
    # Garantir que tipo__nome não seja None
    tipos_data = [item for item in tipos_data if item['tipo__nome'] is not None]
    
    # Calcular porcentagens para cada tipo
    total_count = sum(item['count'] for item in tipos_data)
    for item in tipos_data:
        item['percentage'] = round((item['count'] / total_count) * 100, 1) if total_count > 0 else 0
    
    # Dados para o gráfico de preço médio por tipo
    preco_medio_por_tipo = Fitoterapico.objects.values('tipo__nome').annotate(avg_price=Avg('preco'))
    # Garantir que tipo__nome não seja None
    preco_medio_por_tipo = [item for item in preco_medio_por_tipo if item['tipo__nome'] is not None]
    
    # Dados para o gráfico de evolução do inventário ao longo do tempo
    # Últimos 30 dias
    data_limite = timezone.now() - timedelta(days=30)
    inventario_historico = FitoterapicoInventario.objects.filter(
        created_at__gte=data_limite
    ).annotate(
        data=TruncDate('created_at')
    ).values('data').annotate(
        total_count=Sum('fitoterapico_count'),
        total_value=Sum('fitoterapico_value')
    ).order_by('data')
    
    # Se não houver registros de inventário, criar um registro inicial
    if not inventario_historico.exists():
        # Criar um registro de inventário para hoje
        from fitoterapico.signals import fitoterapico_inventario_update
        fitoterapico_inventario_update()
        
        # Buscar novamente os dados de inventário
        inventario_historico = FitoterapicoInventario.objects.filter(
            created_at__gte=data_limite
        ).annotate(
            data=TruncDate('created_at')
        ).values('data').annotate(
            total_count=Sum('fitoterapico_count'),
            total_value=Sum('fitoterapico_value')
        ).order_by('data')
    
    # Dados para o gráfico de distribuição de preços
    faixas_preco = [
        {'min': 0, 'max': 50, 'label': 'R$0-50'},
        {'min': 50, 'max': 100, 'label': 'R$50-100'},
        {'min': 100, 'max': 150, 'label': 'R$100-150'},
        {'min': 150, 'max': 200, 'label': 'R$150-200'},
        {'min': 200, 'max': float('inf'), 'label': 'R$200+'},
    ]
    
    distribuicao_precos = []
    for faixa in faixas_preco:
        count = Fitoterapico.objects.filter(preco__gte=faixa['min'], preco__lt=faixa['max']).count()
        distribuicao_precos.append({'label': faixa['label'], 'count': count})
    
    # Total de fitoterápicos e valor total
    total_fitoterapicos = Fitoterapico.objects.count()
    valor_total = Fitoterapico.objects.aggregate(total=Sum('preco'))['total'] or 0
    
    # Converter datas para string no formato ISO para serialização JSON
    inventario_historico_list = []
    for item in inventario_historico:
        inventario_historico_list.append({
            'data': item['data'].isoformat() if item['data'] else '',
            'total_count': item['total_count'] or 0,
            'total_value': float(item['total_value'] or 0)
        })
    
    context = {
        'tipos_data': list(tipos_data),
        'preco_medio_por_tipo': list(preco_medio_por_tipo),
        'inventario_historico': inventario_historico_list,
        'distribuicao_precos': distribuicao_precos,
        'total_fitoterapicos': total_fitoterapicos,
        'valor_total': valor_total,
    }
    
    return render(request, 'dashboard.html', context)