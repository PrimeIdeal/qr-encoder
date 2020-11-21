import pytest

from encode.data_encoder import (
    numeric_encoder,
    alphanumeric_encoder,
    bytes_encoder
)


@pytest.fixture(scope='function')
def numeric_zeros(request):
    test_length, test_ec = request.param
    test_msg = ''.join('0' for _ in range(test_length))
    return numeric_encoder(test_msg, test_ec)


@pytest.fixture(scope='function')
def alphanumeric_zeros(request):
    test_length, test_ec = request.param
    test_msg = ''.join('0' for _ in range(test_length))
    return alphanumeric_encoder(test_msg, test_ec)


@pytest.fixture(scope='function')
def bytes_zeros(request):
    test_length, test_ec = request.param
    test_msg = ''.join('0' for _ in range(test_length))
    return bytes_encoder(test_msg, test_ec)
