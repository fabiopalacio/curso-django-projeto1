import pytest  # type: ignore


from .base import AuthorsBaseTest


@pytest.mark.functionaltest
class AuthorsRegisterFunctionalTest(AuthorsBaseTest):

    def test_the_test(self):
        self.fail()
