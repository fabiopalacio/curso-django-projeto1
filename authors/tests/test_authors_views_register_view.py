
from django.test import TestCase  # type: ignore
from django.urls import reverse  # type: ignore

# Class to check the register view behaviour


class RegisterViewTest(TestCase):
    # TEST to check if the view raises 404 status code when
    # a get request is made
    def test_get_register_create_view_raises_404_get_request(self):
        # Getting the url to the view
        url = reverse('authors:register_create')
        # Getting the view. Expect to receive 404 status code
        response = self.client.get(url)

        # Assertions:
        # Check if the response status code is 404
        self.assertEqual(
            404,
            response.status_code,
            msg="GET register_create VIEW: Expecting 404 error. "
            f"Received: {response.status_code}.",)
