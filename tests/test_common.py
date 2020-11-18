import pytest

from encode.common import (
    select_encoding,
    select_encoder
)
from encode.data_encoder import (
    alphanumeric_encoder,
    bytes_encoder,
    numeric_encoder
)


class TestSelectEncoding:
    """
    Test class for the select_encoding() function.
    """

    @pytest.mark.parametrize(
        'test_msg, expected',
        [
            ('00111', 'numeric'),
            ('GOOD AFTERNOON AGENT 47.', 'alphanumeric'),
            ('Good afternoon Agent 47.', 'byte'),
            ('NEW\nLINE', 'byte'),
            (''.join('a' for _ in range(7089)), 'byte')
        ],
        ids=[
            'Numeric',
            'Alphanumeric',
            'Byte - lowercase chars',
            'Byte - char not allowed for alphanumeric',
            'Byte - length just under threshold'
        ]
    )
    def test_valid_strings(self, test_msg, expected):
        assert select_encoding(test_msg) == expected

    def test_string_over_valid_length(self):
        test_msg = ''.join('0' for _ in range(7090))

        with pytest.raises(ValueError) as error_msg:
            select_encoding(test_msg)

        assert str(error_msg.value) == 'Input exceeds maximum encoding length.'


class TestSelectEncoder:
    """
    Test class for the select_encoder() function.
    """

    @pytest.mark.parametrize(
        'test_msg, corr_lvl, encoder_type',
        [
            ('00111', 'M', numeric_encoder),
            ('GOOD AFTERNOON AGENT 47.', 'l', alphanumeric_encoder),
            ('Good afternoon Agent 47.', 'q', bytes_encoder)
        ],
        ids=[
            'Numeric',
            'Alphanumeric - lowercase correction level',
            'Bytes - lowercase correction level'
        ]
    )
    def test_correct_encoder(self, test_msg, corr_lvl, encoder_type):
        test_encoder = select_encoder(test_msg, corr_lvl)

        assert isinstance(test_encoder, encoder_type)
        assert test_encoder.message == test_msg
        assert test_encoder.correction_level == corr_lvl.upper()

    @pytest.mark.parametrize(
        'bad_msg, corr_lvl',
        [
            (None, 'H'),
            (bytes('Good afternoon Agent 47.', 'utf-8'), 'L')
        ],
        ids=[
            'Message is None',
            'Message is bytes'
        ]
    )
    def test_bad_msg(self, bad_msg, corr_lvl):
        with pytest.raises(TypeError) as error_msg:
            select_encoder(bad_msg, corr_lvl)

        assert str(error_msg.value) == f'Message is not a string: {bad_msg}.'

    def test_bad_corr_lvl(self):
        with pytest.raises(ValueError) as error_msg:
            select_encoder('r', 'J')

        assert str(error_msg.value) == 'Unrecognized correction level: J.'
