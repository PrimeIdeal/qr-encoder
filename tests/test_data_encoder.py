import pytest

from encode.data_encoder import (
    alphanumeric_encoder,
    bytes_encoder,
    numeric_encoder
)


class TestGetVersion:

    @pytest.mark.parametrize(
        'test_msg, test_ec, expected',
        [
            (''.join('0' for _ in range(41)), 'L', 1),
            (''.join('1' for _ in range(432)), 'M', 9),
            (''.join('2' for _ in range(1932)), 'Q', 27),
            (''.join('3' for _ in range(2734)), 'H', 38)
        ],
        ids=[
            'Equal to cap - EC level L',
            'Equal to cap - EC level M',
            'Less than cap - EC level Q',
            'Less than cap - EC level H'
        ]
    )
    def test_numeric_valid_msg(self, test_msg, test_ec, expected):
        test_encoder = numeric_encoder(test_msg, test_ec)

        assert test_encoder.get_version() == expected

    def test_numeric_invalid_msg(self):
        test_msg, test_ec = ''.join('4' for _ in range(3599)), 'H'
        test_encoder = numeric_encoder(test_msg, test_ec)
        error_msg = 'Message is too long for specified error correction level.'

        with pytest.raises(ValueError) as error_info:
            test_encoder.get_version()

        assert str(error_info.value) == error_msg

    @pytest.mark.parametrize(
        'test_msg, test_ec, expected',
        [
            (''.join('0' for _ in range(25)), 'L', 1),
            (''.join('1' for _ in range(262)), 'M', 9),
            (''.join('2' for _ in range(1171)), 'Q', 27),
            (''.join('3' for _ in range(1657)), 'H', 38)
        ],
        ids=[
            'Equal to cap - EC level L',
            'Equal to cap - EC level M',
            'Less than cap - EC level Q',
            'Less than cap - EC level H'
        ]
    )
    def test_alphanumeric_valid_msg(self, test_msg, test_ec, expected):
        test_encoder = alphanumeric_encoder(test_msg, test_ec)

        assert test_encoder.get_version() == expected

    def test_alphanumeric_invalid_msg(self):
        test_msg, test_ec = ''.join('4' for _ in range(2181)), 'H'
        test_encoder = alphanumeric_encoder(test_msg, test_ec)
        error_msg = 'Message is too long for specified error correction level.'

        with pytest.raises(ValueError) as error_info:
            test_encoder.get_version()

        assert str(error_info.value) == error_msg

    @pytest.mark.parametrize(
        'test_msg, test_ec, expected',
        [
            (''.join('0' for _ in range(17)), 'L', 1),
            (''.join('1' for _ in range(180)), 'M', 9),
            (''.join('2' for _ in range(804)), 'Q', 27),
            (''.join('3' for _ in range(1138)), 'H', 38)
        ],
        ids=[
            'Equal to cap - EC level L',
            'Equal to cap - EC level M',
            'Less than cap - EC level Q',
            'Less than cap - EC level H'
        ]
    )
    def test_bytes_valid_msg(self, test_msg, test_ec, expected):
        test_encoder = bytes_encoder(test_msg, test_ec)

        assert test_encoder.get_version() == expected

    def test_bytes_invalid_msg(self):
        test_msg, test_ec = ''.join('4' for _ in range(1499)), 'H'
        test_encoder = bytes_encoder(test_msg, test_ec)
        error_msg = 'Message is too long for specified error correction level.'

        with pytest.raises(ValueError) as error_info:
            test_encoder.get_version()

        assert str(error_info.value) == error_msg
