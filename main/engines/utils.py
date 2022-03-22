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
