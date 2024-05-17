
from django.test import TestCase

from django.urls import reverse


class RegisterViewTest(TestCase):
    def test_get_register_create_view_raises_404(self):
        url = reverse('authors:create')
        response = self.client.get(url)

        self.assertEqual(404, response.status_code)
