def select_encoding(msg: str) -> str:
    """
    Determines which type of text encoding will be used for the message.

    If msg is strictly decimal, specifies numeric encoding. If msg is composed
    of numbers, uppercase letters, and characters in
    {' ', '$', '%', '*', '+', '-', '.', '/', ':'}, specifies alphanumeric
    encoding. Otherwise, specifies byte encoding.

    Parameters
    ----------
    msg : str
        Text to be encoded as a QR code.

    Returns
    -------
    str
        Specified encoding mode.

    Raises
    ------
    ValueError
        Input is too long to be encoded.
    """
    if len(msg) > 7089:
        raise ValueError('Input exceeds maximum encoding length.')

    allowed_chars = {' ', '$', '%', '*', '+', '-', '.', '/', ':'}
    if msg.isdecimal():
        return 'numeric'

    for char in msg:
        if (char.isalpha() and char.islower()) or \
            (not char.isalpha() and not char.isdecimal()
             and char not in allowed_chars):
            return 'byte'

    return 'alphanumeric'


def read_from_file(path: str) -> str:
    pass
