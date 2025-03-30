from django.db import models
from django.core.validators import MinValueValidator


class Tipo(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

class Fitoterapico(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    tipo = models.ForeignKey(Tipo, on_delete=models.PROTECT, related_name='fitoterapico_tipo')
    especie = models.CharField(max_length=100)
    familia = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.TextField()
    propriedades = models.TextField()
    indicacao = models.TextField()
    modo_uso = models.TextField()
    dosagem = models.CharField(max_length=100, blank=True, null=True)
    efeito_colateral = models.TextField(blank=True, null=True)
    preco = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0)])
    foto = models.ImageField(upload_to='fitoterapico/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']


class FitoterapicoInventario(models.Model):
    fitoterapico_count = models.IntegerField()
    fitoterapico_value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.fitoterapico_count} - {self.fitoterapico_value}'
    