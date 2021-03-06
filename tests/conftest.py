import pytest

from encode.data_encoder import (
    AlphanumericEncoder,
    BytesEncoder,
    NumericEncoder,
)


def _get_test_msg(test_length: str, char: str = '0') -> str:
    """
    Helper function: returns a test string.

    Parameters
    ----------
    test_length :  str
        Length of test string.
    char : str, optional
        Character with which to create the string (defaults to '0').

    Returns
    -------
    str
        Test string.
    """
    return ''.join(char for _ in range(test_length))


@pytest.fixture(scope='function')
def numeric_zeros(request):
    test_length, test_ec = request.param
    test_msg = _get_test_msg(test_length)
    return NumericEncoder(test_msg, test_ec)


@pytest.fixture(scope='function')
def alphanumeric_zeros(request):
    test_length, test_ec = request.param
    test_msg = _get_test_msg(test_length)
    return AlphanumericEncoder(test_msg, test_ec)


@pytest.fixture(scope='function')
def bytes_zeros(request):
    test_length, test_ec = request.param
    test_msg = _get_test_msg(test_length)
    return BytesEncoder(test_msg, test_ec)
