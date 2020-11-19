import pytest

from encode.data_encoder import (
    alphanumeric_encoder,
    bytes_encoder,
    numeric_encoder
)


class TestConstructor:

    @pytest.mark.parametrize(
        'test_len, test_ec, version, cap',
        [
            (41, 'L', 1, 41),
            (432, 'M', 9, 432),
            (1932, 'Q', 27, 1933),
            (2734, 'H', 38, 2735)
        ],
        ids=[
            'Equal to cap - EC level L',
            'Equal to cap - EC level M',
            'Less than cap - EC level Q',
            'Less than cap - EC level H'
        ]
    )
    def test_numeric_valid_msg(self, test_len, test_ec, version, cap):
        test_msg = ''.join('0' for _ in range(test_len))
        test_encoder = numeric_encoder(test_msg, test_ec)

        assert test_encoder.version == version
        assert test_encoder.bit_cap == cap

    def test_numeric_invalid_msg(self):
        test_msg, test_ec = ''.join('4' for _ in range(3599)), 'H'
        error_msg = 'Message is too long for specified error correction level.'

        with pytest.raises(ValueError) as error_info:
            numeric_encoder(test_msg, test_ec)

        assert str(error_info.value) == error_msg

    @pytest.mark.parametrize(
        'test_len, test_ec, version, cap',
        [
            (25, 'L', 1, 25),
            (262, 'M', 9, 262),
            (1171, 'Q', 27, 1172),
            (1657, 'H', 38, 1658)
        ],
        ids=[
            'Equal to cap - EC level L',
            'Equal to cap - EC level M',
            'Less than cap - EC level Q',
            'Less than cap - EC level H'
        ]
    )
    def test_alphanumeric_valid_msg(self, test_len, test_ec, version, cap):
        test_msg = ''.join('0' for _ in range(test_len))
        test_encoder = alphanumeric_encoder(test_msg, test_ec)

        assert test_encoder.version == version
        assert test_encoder.bit_cap == cap

    def test_alphanumeric_invalid_msg(self):
        test_msg, test_ec = ''.join('4' for _ in range(2181)), 'H'
        error_msg = 'Message is too long for specified error correction level.'

        with pytest.raises(ValueError) as error_info:
            alphanumeric_encoder(test_msg, test_ec)

        assert str(error_info.value) == error_msg

    @pytest.mark.parametrize(
        'test_len, test_ec, version, cap',
        [
            (17, 'L', 1, 17),
            (180, 'M', 9, 180),
            (804, 'Q', 27, 805),
            (1138, 'H', 38, 1139)
        ],
        ids=[
            'Equal to cap - EC level L',
            'Equal to cap - EC level M',
            'Less than cap - EC level Q',
            'Less than cap - EC level H'
        ]
    )
    def test_bytes_valid_msg(self, test_len, test_ec, version, cap):
        test_msg = ''.join('0' for _ in range(test_len))
        test_encoder = bytes_encoder(test_msg, test_ec)

        assert test_encoder.version == version
        assert test_encoder.bit_cap == cap

    def test_bytes_invalid_msg(self):
        test_msg, test_ec = ''.join('4' for _ in range(1499)), 'H'
        error_msg = 'Message is too long for specified error correction level.'

        with pytest.raises(ValueError) as error_info:
            bytes_encoder(test_msg, test_ec)

        assert str(error_info.value) == error_msg
