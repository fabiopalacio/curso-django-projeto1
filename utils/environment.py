
import os


def get_env_variables(variable_name, default_value=''):
    return os.environ.get(variable_name, default_value)


def parse_comma_sep_to_list(comma_sep_str):
    if not comma_sep_str or not isinstance(comma_sep_str, str):
        return []
    return [string.strip() for string in comma_sep_str.split(',') if string]
