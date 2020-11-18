from encode.data_encoder import (
    alphanumeric_encoder,
    bytes_encoder,
    numeric_encoder,
    qr_encoder
)


def select_encoding(msg: str) -> str:
    """
    Determines which type of text encoding will be used for the message.

    If msg is strictly decimal, specifies numeric encoding. If msg is composed
    of numbers, uppercase letters, and characters in
    (' ', '$', '%', '*', '+', '-', '.', '/', ':'), specifies alphanumeric
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

    if msg.isdecimal():
        return 'numeric'

    for char in msg:
        if (char.isalpha() and char.islower()) or \
            (not char.isalpha() and not char.isdecimal()
             and char not in ALPHANUMERIC_CHARS):
            return 'byte'

    return 'alphanumeric'


def select_encoder(msg: str, correction_level: str) -> qr_encoder:
    """
    Selects an appropriate QR encoder for the message input.

    Parameters
    ----------
    msg: str
        Text to be encoded as a QR code.
    correction_level : str
        Specified error correction level.

    Returns
    -------
    qr_encoder
        qr_encoder object for the message.

    Raises
    ------
    TypeError
        Input is not a string.
    ValueError
        Correction level not in ('L', 'M', 'Q', 'H')
    """
    if not isinstance(msg, str):
        raise TypeError(f'Message is not a string: {msg}.')
    if correction_level.upper() not in CORRECTION_LEVELS:
        raise ValueError(f'Unrecognized correction level: {correction_level}.')

    encoding = select_encoding(msg)
    if encoding == 'numeric':
        return numeric_encoder(msg, correction_level.upper())
    if encoding == 'alphanumeric':
        return alphanumeric_encoder(msg, correction_level.upper())
    else:
        return bytes_encoder(msg, correction_level.upper())


ALPHANUMERIC_CHARS = {' ', '$', '%', '*', '+', '-', '.', '/', ':'}

CORRECTION_LEVELS = {'L', 'M', 'Q', 'H'}

CHAR_CAP = {}
