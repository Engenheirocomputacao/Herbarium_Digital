from django.db.models.signals import pre_save,post_save, post_delete
from django.db.models import Sum
from django.dispatch import receiver
from fitoterapico.models import Fitoterapico, FitoterapicoInventario


def fitoterapico_inventario_update():
    fitoterapico_count = Fitoterapico.objects.count()
    fitoterapico_value = Fitoterapico.objects.aggregate(total_value=Sum('preco'))['total_value']
    # Garantir que fitoterapico_value não seja None
    if fitoterapico_value is None:
        fitoterapico_value = 0.0
    FitoterapicoInventario.objects.create(fitoterapico_count=fitoterapico_count, fitoterapico_value=fitoterapico_value)

@receiver(pre_save, sender=Fitoterapico)
def fitoterapico_pre_save(sender, instance, **kwargs):
    if not instance.bio:
        instance.bio = 'Bio gerada automaticamente!'
@receiver(post_save, sender=Fitoterapico)
def fitoterapico_post_save(sender, instance, **kwargs):
    fitoterapico_inventario_update()


@receiver(post_delete, sender=Fitoterapico)
def fitoterapico_post_delete(sender, instance, **kwargs):
    fitoterapico_inventario_update()

