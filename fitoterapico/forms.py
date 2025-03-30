from django import forms
from fitoterapico.models import Fitoterapico
from django.core.validators import MinValueValidator
import re


class FitoterapicoModelForm(forms.ModelForm):
    class Meta:
        model = Fitoterapico
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do fitoterápico'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'especie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Espécie'}),
            'familia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Família'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descrição detalhada'}),
            'propriedades': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Propriedades medicinais'}),
            'indicacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Indicações de uso'}),
            'modo_uso': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Como utilizar'}),
            'dosagem': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dosagem recomendada'}),
            'efeito_colateral': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Possíveis efeitos colaterais'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço em R$', 'min': '0', 'step': '0.01'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Informações biológicas adicionais'}),
        }
        error_messages = {
            'nome': {
                'required': 'O nome do fitoterápico é obrigatório.',
                'max_length': 'O nome não pode ter mais de 100 caracteres.'
            },
            'tipo': {
                'required': 'O tipo é obrigatório.',
            },
            'especie': {
                'required': 'A espécie é obrigatória.',
                'max_length': 'A espécie não pode ter mais de 100 caracteres.'
            },
            'descricao': {
                'required': 'A descrição é obrigatória.'
            },
            'propriedades': {
                'required': 'As propriedades são obrigatórias.'
            },
            'indicacao': {
                'required': 'A indicação é obrigatória.'
            },
            'modo_uso': {
                'required': 'O modo de uso é obrigatório.'
            }
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if nome and len(nome) < 3:
            raise forms.ValidationError('O nome deve ter pelo menos 3 caracteres.')
        return nome

    def clean_preco(self):
        preco = self.cleaned_data.get('preco')
        if preco is not None and preco < 0:
            raise forms.ValidationError('O preço não pode ser negativo.')
        return preco
        
    def clean_especie(self):
        especie = self.cleaned_data.get('especie')
        if especie and not re.match(r'^[A-Za-z\s\-\.]+$', especie):
            raise forms.ValidationError('A espécie deve conter apenas letras, espaços, hífens e pontos.')
        return especie