

from unittest import TestCase
from parameterized import parameterized  # type: ignore

from utils.strings import is_positive_number


class UtilsStringsTest(TestCase):

    @parameterized.expand([
        (1, True),
        (1.1, True),
        ('2', True),
        ('2.2', True),
        (-3, False),
        ('-4', False),
        ('text', False),
        (True, False),
        (0, False),

    ])
    def test_is_positive_number_returns_false_if_negative_number(
            self,
            number,
            exp_result
    ):
        result = is_positive_number(number)

        self.assertEqual(result, exp_result)
