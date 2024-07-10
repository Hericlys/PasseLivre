def clean_space(string: str) -> str:
    """
    Removes leading and trailing spaces and
    replaces multiple spaces with a single space.

    Args:
        string str: string.

    Returns:
        str: new string
    """
    new_string = ' '.join(string.split())
    return new_string
