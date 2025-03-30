from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserRegistrationTest(TestCase):
    def setUp(self):
        self.register_url = reverse('registro')
        self.login_url = reverse('login')
        self.user_data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
    
    def test_registration_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registro.html')
    
    def test_registration_creates_user(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso
        self.assertRedirects(response, self.login_url)
        self.assertTrue(User.objects.filter(username='testuser').exists())
    
    def test_registration_invalid_data(self):
        # Senhas não coincidem
        invalid_data = self.user_data.copy()
        invalid_data['password2'] = 'diferentpassword'
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, 200)  # Permanece na mesma página
        self.assertFalse(User.objects.filter(username='testuser').exists())


class UserLoginTest(TestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.fitoterapico_list_url = reverse('fitoterapico_list')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
    
    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
    
    def test_login_valid_user(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso
        self.assertRedirects(response, self.fitoterapico_list_url)
    
    def test_login_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Permanece na mesma página


class UserLogoutTest(TestCase):
    def setUp(self):
        self.logout_url = reverse('logout')
        self.fitoterapico_list_url = reverse('fitoterapico_list')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        self.client.login(username='testuser', password='testpassword123')
    
    def test_logout_redirects(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso
        self.assertRedirects(response, self.fitoterapico_list_url)
