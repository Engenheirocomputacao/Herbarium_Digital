from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Tipo, Fitoterapico, FitoterapicoInventario
from .forms import FitoterapicoModelForm
from django.core.files.uploadedfile import SimpleUploadedFile


class TipoModelTest(TestCase):
    def setUp(self):
        self.tipo = Tipo.objects.create(nome='Chá')
    
    def test_tipo_creation(self):
        self.assertEqual(self.tipo.nome, 'Chá')
        self.assertTrue(isinstance(self.tipo, Tipo))
    
    def test_tipo_str(self):
        self.assertEqual(str(self.tipo), 'Chá')


class FitoterapicoModelTest(TestCase):
    def setUp(self):
        self.tipo = Tipo.objects.create(nome='Chá')
        self.fitoterapico = Fitoterapico.objects.create(
            nome='Camomila',
            tipo=self.tipo,
            especie='Matricaria chamomilla',
            familia='Asteraceae',
            descricao='Planta medicinal com propriedades calmantes',
            propriedades='Calmante, anti-inflamatória',
            indicacao='Ansiedade, insônia',
            modo_uso='Infusão',
            dosagem='1 colher de sopa por xícara',
            efeito_colateral='Raramente causa reações alérgicas',
            preco=15.50
        )
    
    def test_fitoterapico_creation(self):
        self.assertEqual(self.fitoterapico.nome, 'Camomila')
        self.assertEqual(self.fitoterapico.tipo, self.tipo)
        self.assertEqual(self.fitoterapico.especie, 'Matricaria chamomilla')
        self.assertEqual(self.fitoterapico.preco, 15.50)
        self.assertTrue(isinstance(self.fitoterapico, Fitoterapico))
    
    def test_fitoterapico_str(self):
        self.assertEqual(str(self.fitoterapico), 'Camomila')


class FitoterapicoInventarioModelTest(TestCase):
    def setUp(self):
        self.inventario = FitoterapicoInventario.objects.create(
            fitoterapico_count=10,
            fitoterapico_value=150.00
        )
    
    def test_inventario_creation(self):
        self.assertEqual(self.inventario.fitoterapico_count, 10)
        self.assertEqual(self.inventario.fitoterapico_value, 150.00)
        self.assertTrue(isinstance(self.inventario, FitoterapicoInventario))
    
    def test_inventario_str(self):
        self.assertEqual(str(self.inventario), '10 - 150.0')


class FitoterapicoFormTest(TestCase):
    def setUp(self):
        self.tipo = Tipo.objects.create(nome='Chá')
        self.form_data = {
            'nome': 'Camomila',
            'tipo': self.tipo.id,
            'especie': 'Matricaria chamomilla',
            'familia': 'Asteraceae',
            'descricao': 'Planta medicinal com propriedades calmantes',
            'propriedades': 'Calmante, anti-inflamatória',
            'indicacao': 'Ansiedade, insônia',
            'modo_uso': 'Infusão',
            'dosagem': '1 colher de sopa por xícara',
            'efeito_colateral': 'Raramente causa reações alérgicas',
            'preco': 15.50
        }
    
    def test_valid_form(self):
        form = FitoterapicoModelForm(data=self.form_data)
        self.assertTrue(form.is_valid())
    
    def test_nome_validation(self):
        # Nome muito curto
        self.form_data['nome'] = 'Ca'
        form = FitoterapicoModelForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nome', form.errors)
        
        # Nome muito longo
        self.form_data['nome'] = 'C' * 101
        form = FitoterapicoModelForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nome', form.errors)
    
    def test_preco_validation(self):
        # Preço menor que 1
        self.form_data['preco'] = 0.5
        form = FitoterapicoModelForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('preco', form.errors)
    
    def test_especie_validation(self):
        # Espécie com caracteres inválidos
        self.form_data['especie'] = 'Matricaria123'
        form = FitoterapicoModelForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('especie', form.errors)


class FitoterapicoViewTest(TestCase):
    def setUp(self):
        # Criar um usuário para testar views protegidas
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Criar tipo e fitoterapico para testes
        self.tipo = Tipo.objects.create(nome='Chá')
        self.fitoterapico = Fitoterapico.objects.create(
            nome='Camomila',
            tipo=self.tipo,
            especie='Matricaria chamomilla',
            familia='Asteraceae',
            descricao='Planta medicinal com propriedades calmantes',
            propriedades='Calmante, anti-inflamatória',
            indicacao='Ansiedade, insônia',
            modo_uso='Infusão',
            dosagem='1 colher de sopa por xícara',
            efeito_colateral='Raramente causa reações alérgicas',
            preco=15.50
        )
        
        # Dados para criar novo fitoterapico
        self.form_data = {
            'nome': 'Boldo',
            'tipo': self.tipo.id,
            'especie': 'Peumus boldus',
            'familia': 'Monimiaceae',
            'descricao': 'Planta medicinal para problemas digestivos',
            'propriedades': 'Digestiva, hepatoprotetora',
            'indicacao': 'Problemas digestivos, dor de estômago',
            'modo_uso': 'Infusão',
            'dosagem': '1 colher de sopa por xícara',
            'efeito_colateral': 'Pode causar irritação gástrica em excesso',
            'preco': 12.50
        }
    
    def test_fitoterapico_list_view(self):
        response = self.client.get(reverse('fitoterapico_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fitoterapico.html')
        self.assertContains(response, 'Camomila')
    
    def test_fitoterapico_detail_view(self):
        response = self.client.get(reverse('fitoterapico_detail', kwargs={'pk': self.fitoterapico.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fitoterapico_detail.html')
        self.assertContains(response, 'Camomila')
        self.assertContains(response, 'Matricaria chamomilla')
    
    def test_novo_fitoterapico_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('novo_fitoterapico'))
        self.assertRedirects(response, '/login/?next=/novo_fitoterapico/')
    
    def test_novo_fitoterapico_view_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('novo_fitoterapico'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'novo_fitoterapico.html')
    
    def test_create_fitoterapico(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('novo_fitoterapico'), self.form_data)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso
        self.assertTrue(Fitoterapico.objects.filter(nome='Boldo').exists())
    
    def test_update_fitoterapico_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('fitoterapico_update', kwargs={'pk': self.fitoterapico.pk}))
        self.assertRedirects(response, f'/login/?next=/fitoterapico/{self.fitoterapico.pk}/update/')
    
    def test_update_fitoterapico_view_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('fitoterapico_update', kwargs={'pk': self.fitoterapico.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fitoterapico_update.html')
    
    def test_update_fitoterapico(self):
        self.client.login(username='testuser', password='testpassword')
        updated_data = self.form_data.copy()
        updated_data['nome'] = 'Camomila Atualizada'
        response = self.client.post(
            reverse('fitoterapico_update', kwargs={'pk': self.fitoterapico.pk}),
            updated_data
        )
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso
        self.fitoterapico.refresh_from_db()
        self.assertEqual(self.fitoterapico.nome, 'Camomila Atualizada')
    
    def test_delete_fitoterapico_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('fitoterapico_delete', kwargs={'pk': self.fitoterapico.pk}))
        self.assertRedirects(response, f'/login/?next=/fitoterapico/{self.fitoterapico.pk}/delete/')
    
    def test_delete_fitoterapico_view_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('fitoterapico_delete', kwargs={'pk': self.fitoterapico.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fitoterapico_delete.html')
    
    def test_delete_fitoterapico(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('fitoterapico_delete', kwargs={'pk': self.fitoterapico.pk}))
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso
        self.assertFalse(Fitoterapico.objects.filter(pk=self.fitoterapico.pk).exists())
