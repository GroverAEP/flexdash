# mi_app/tests.py
from django.test import TestCase
from django.urls import reverse

class IndexViewTest(TestCase):
    def test_index_status_code(self):
        response = self.client.get('/index/')  # o usa reverse('index') si tiene `name=`
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hola a todos los que operan en este servicio")
    