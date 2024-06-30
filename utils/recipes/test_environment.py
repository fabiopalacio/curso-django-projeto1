
from unittest import TestCase
from utils.environment import parse_comma_sep_to_list


class EnvironemntsUtilsTest(TestCase):
    def test_parse_comma_sep_to_list_returns_list(self):
        my_string = 'first,second,third,fourth'
        my_list = ['first', 'second', 'third', 'fourth']
        func_return = parse_comma_sep_to_list(my_string)

        self.assertEqual(
            my_list,
            func_return,
            msg='UTILS ENVIRONMENT - PARSE FUNC: Wrong list returned.'
            f'Expected: {my_list}. '
            f'Found: {func_return}.'
        )

    def test_parse_comma_sep_to_list_returns_empty_list(self):
        func_return = parse_comma_sep_to_list(None)
        self.assertEqual(
            [],
            func_return,
            msg='UTILS ENVIRONMENT - PARSE FUNC: Wrong list returned.'
            'Expected: []. '
            f'Found: {func_return}.'
        )

        func_return = parse_comma_sep_to_list(123)
        self.assertEqual(
            [],
            func_return,
            msg='UTILS ENVIRONMENT - PARSE FUNC: Wrong list returned.'
            'Expected: []. '
            f'Found: {func_return}.'
        )
