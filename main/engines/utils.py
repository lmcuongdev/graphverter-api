from typing import Mapping


def replace_variables(text: str, variables: Mapping[str, str]) -> str:
    """
    Example:
        text: 'My name is $name'
        variables: {'name': 'Ryan'}
    Result: 'My name is Ryan'
    """
    result = text
    for var, value in variables.items():
        result = result.replace(f'${var}', str(value))

    return result


def trim_data(data: dict):
    """Use this function in pre_load if needed."""
    for k, v in data.items():
        if isinstance(data[k], str):
            data[k] = ' '.join(data[k].split())
    return data
