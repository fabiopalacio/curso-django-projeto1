
import os


def get_env_variables(variable_name, default_value=''):
    return os.environ.get(variable_name, default_value)


def parse_comma_sep_to_list(comma_sep_str):
    if not comma_sep_str or not isinstance(comma_sep_str, str):
        return []
    return [string.strip() for string in comma_sep_str.split(',') if string]


if __name__ == 'main':
    from dotenv import load_dotenv
    load_dotenv()
    print(parse_comma_sep_to_list(get_env_variables('ALLOWED_HOSTS')))
    print(parse_comma_sep_to_list(''))
    print(parse_comma_sep_to_list(123))
    print(parse_comma_sep_to_list('a,b,c'))
