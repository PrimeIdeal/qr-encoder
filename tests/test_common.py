import pytest

from encode.common import select_encoding


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
