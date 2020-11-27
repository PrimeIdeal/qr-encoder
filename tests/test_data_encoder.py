import pytest

from encode.data_encoder import (
    AlphanumericEncoder,
    BytesEncoder,
    NumericEncoder,
)


class TestConstructor:

    @pytest.mark.parametrize(
        'numeric_zeros, version, cap',
        [
            ((41, 'L'), 1, 41),
            ((432, 'M'), 9, 432),
            ((1932, 'Q'), 27, 1933),
            ((2734, 'H'), 38, 2735)
        ],
        ids=[
            'Equal to cap - EC level L',
            'Equal to cap - EC level M',
            'Less than cap - EC level Q',
            'Less than cap - EC level H'
        ],
        indirect=['numeric_zeros']
    )
    def test_numeric_valid_msg(self, numeric_zeros, version, cap):
        assert numeric_zeros.version == version
        assert numeric_zeros.bit_cap == cap

    def test_numeric_invalid_msg(self):
        test_msg, test_ec = ''.join('4' for _ in range(3599)), 'H'
        error_msg = 'Message too long for correction level H.'

        with pytest.raises(ValueError) as error_info:
            NumericEncoder(test_msg, test_ec)

        assert str(error_info.value) == error_msg

    @pytest.mark.parametrize(
        'alphanumeric_zeros, version, cap',
        [
            ((25, 'L'), 1, 25),
            ((262, 'M'), 9, 262),
            ((1171, 'Q'), 27, 1172),
            ((1657, 'H'), 38, 1658)
        ],
        ids=[
            'Equal to cap - EC level L',
            'Equal to cap - EC level M',
            'Less than cap - EC level Q',
            'Less than cap - EC level H'
        ],
        indirect=['alphanumeric_zeros']
    )
    def test_alphanumeric_valid_msg(self, alphanumeric_zeros, version, cap):
        assert alphanumeric_zeros.version == version
        assert alphanumeric_zeros.bit_cap == cap

    def test_alphanumeric_invalid_msg(self):
        test_msg, test_ec = ''.join('4' for _ in range(2181)), 'H'
        error_msg = 'Message too long for correction level H.'

        with pytest.raises(ValueError) as error_info:
            AlphanumericEncoder(test_msg, test_ec)

        assert str(error_info.value) == error_msg

    @pytest.mark.parametrize(
        'bytes_zeros, version, cap',
        [
            ((17, 'L'), 1, 17),
            ((180, 'M'), 9, 180),
            ((804, 'Q'), 27, 805),
            ((1138, 'H'), 38, 1139)
        ],
        ids=[
            'Equal to cap - EC level L',
            'Equal to cap - EC level M',
            'Less than cap - EC level Q',
            'Less than cap - EC level H'
        ],
        indirect=['bytes_zeros']
    )
    def test_bytes_valid_msg(self, bytes_zeros, version, cap):
        assert bytes_zeros.version == version
        assert bytes_zeros.bit_cap == cap

    def test_bytes_invalid_msg(self):
        test_msg, test_ec = ''.join('4' for _ in range(1499)), 'H'
        error_msg = 'Message too long for correction level H.'

        with pytest.raises(ValueError) as error_info:
            BytesEncoder(test_msg, test_ec)

        assert str(error_info.value) == error_msg


class TestGetPrefix:

    @pytest.mark.parametrize(
        'numeric_zeros, expected',
        [
            ((3, 'L'), '00010000000011'),
            ((427, 'M'), '00010110101011'),
            ((532, 'Q'), '0001001000010100'),
            ((2714, 'H'), '000100101010011010')
        ],
        ids=[
            '1L - 10 bit char count indicator',
            '9M - 10 bit char count indicator',
            '13Q - 12 bit char count indicator',
            '38H - 14 bit char count indicator'
        ],
        indirect=['numeric_zeros']
    )
    def test_numeric_prefix(self, numeric_zeros, expected):
        assert numeric_zeros.get_prefix() == expected

    @pytest.mark.parametrize(
        'alphanumeric_zeros, expected',
        [
            ((7, 'L'), '0010000000111'),
            ((200, 'M'), '0010011001000'),
            ((512, 'Q'), '001001000000000'),
            ((1592, 'H'), '00100011000111000')
        ],
        ids=[
            '1L - 9 bit char count indicator',
            '8M - 9 bit char count indicator',
            '17Q - 11 bit char count indicator',
            '38H - 13 bit char count indicator'
        ],
        indirect=['alphanumeric_zeros']
    )
    def test_alphanumeric_prefix(self, alphanumeric_zeros, expected):
        assert alphanumeric_zeros.get_prefix() == expected

    @pytest.mark.parametrize(
        'bytes_zeros, expected',
        [
            ((5, 'L'), '010000000101'),
            ((141, 'M'), '010010001101'),
            ((209, 'Q'), '01000000000011010001'),
            ((1112, 'H'), '01000000010001011000')
        ],
        ids=[
            '1L - 8 bit char count indicator',
            '8M - 8 bit char count indicator',
            '13Q - 16 bit char count indicator',
            '38H - 16 bit char count indicator'
        ],
        indirect=['bytes_zeros']
    )
    def test_bytes_prefix(self, bytes_zeros, expected):
        assert bytes_zeros.get_prefix() == expected


class TestEncode:

    @pytest.mark.parametrize(
        'message, expected',
        [
            ('562677', '10001100101010100101'),
            ('56267783', '100011001010101001011010011'),
            ('5626779', '100011001010101001011001'),
            ('562121', '10001100100001111001'),
            ('562063', '10001100100111111'),
            ('562003', '10001100100011')
        ],
        ids=[
            'No padding necessary - all groups 3 digits',
            'No padding necessary - 2 digit group',
            'No padding necessary - 1 digit group',
            'Pad required for 3 digit group',
            'Pad required for 2 digit group',
            'Pad required for 1 digit group'
        ]
    )
    def test_numeric_message(self, message, expected):
        test_encoder = NumericEncoder(message, 'L')
        assert test_encoder.encode() == expected

    @pytest.mark.parametrize(
        'message, expected',
        [
            ('-./:', '1110101111111110111011'),
            ('D7D5', '0100101000001001001110'),
            ('+-./:', '1110011000111110001101101100'),
            ('D7-D5', '0100101000011101000010000101')
        ],
        ids=[
            'Even length - no padding necessary',
            'Even length - padding necessary',
            'Odd length - no padding necessary',
            'Odd length - padding necessary'
        ]
    )
    def test_alphanumeric_message(self, message, expected):
        test_encoder = AlphanumericEncoder(message, 'L')
        assert test_encoder.encode() == expected

    @pytest.mark.parametrize(
        'message, expected',
        [
            ('Ghosst', '010001110110100001101111011100110111001101110100'),
            ('1\n2', '001100010000101000110010')
        ],
        ids=[
            'No escape characters',
            'Escape characters'
        ]
    )
    def test_bytes_message(self, message, expected):
        test_encoder = BytesEncoder(message, 'L')
        assert test_encoder.encode() == expected


class TestGetNumBits:

    @pytest.mark.parametrize(
        'numeric_zeros, expected',
        [
            ((3, 'L'), 152),
            ((427, 'M'), 1456)
        ],
        ids=[
            'Single group',
            'Two groups'
        ],
        indirect=['numeric_zeros']
    )
    def test_numeric_num_bits(self, numeric_zeros, expected):
        assert numeric_zeros.get_num_bits() == expected

    @pytest.mark.parametrize(
        'alphanumeric_zeros, expected',
        [
            ((7, 'L'), 152),
            ((200, 'M'), 1232)
        ],
        ids=[
            'Single group',
            'Two groups'
        ],
        indirect=['alphanumeric_zeros']
    )
    def test_alphanumeric_num_bits(self, alphanumeric_zeros, expected):
        assert alphanumeric_zeros.get_num_bits() == expected

    @pytest.mark.parametrize(
        'bytes_zeros, expected',
        [
            ((5, 'L'), 152),
            ((141, 'M'), 1232)
        ],
        ids=[
            'Single group',
            'Two groups'
        ],
        indirect=['bytes_zeros']
    )
    def test_bytes_num_bits(self, bytes_zeros, expected):
        assert bytes_zeros.get_num_bits() == expected


class TestGetSuffix:

    @pytest.mark.parametrize(
        'numeric_zeros, expected',
        [
            ((427, 'M'), '0'*7 + '1110110000010001'*63),
            ((532, 'Q'), '0'*4 + '1110110000010001'*87 + '11101100'),
            ((2714, 'H'), '0'*4 + '1110110000010001'*400)
        ],
        ids=[
            '9M - 10 bit char count indicator',
            '13Q - 12 bit char count indicator',
            '38H - 14 bit char count indicator'
        ],
        indirect=['numeric_zeros']
    )
    def test_numeric_suffix(self, numeric_zeros, expected):
        test_len = len(numeric_zeros.get_prefix() + numeric_zeros.message)
        assert numeric_zeros.get_suffix(test_len) == expected

    @pytest.mark.parametrize(
        'alphanumeric_zeros, expected',
        [
            ((200, 'M'), '0'*11 + '1110110000010001'*63),
            ((512, 'Q'), '0'*9 + '1110110000010001'*150),
            ((1592, 'H'), '0'*7 + '1110110000010001'*470)
        ],
        ids=[
            '8M - 9 bit char count indicator',
            '17Q - 11 bit char count indicator',
            '38H - 13 bit char count indicator'
        ],
        indirect=['alphanumeric_zeros']
    )
    def test_alphanumeric_suffix(self, alphanumeric_zeros, expected):
        test_len = len(
            alphanumeric_zeros.get_prefix() + alphanumeric_zeros.message
        )
        assert alphanumeric_zeros.get_suffix(test_len) == expected

    @pytest.mark.parametrize(
        'bytes_zeros, expected',
        [
            ((141, 'M'), '0'*7 + '1110110000010001'*67),
            ((209, 'Q'), '0'*11 + '1110110000010001'*107),
            ((1112, 'H'), '0'*4 + '1110110000010001'*500)
        ],
        ids=[
            '8M - 8 bit char count indicator',
            '13Q - 16 bit char count indicator',
            '38H - 16 bit char count indicator'
        ],
        indirect=['bytes_zeros']
    )
    def test_bytes_suffix(self, bytes_zeros, expected):
        test_len = len(bytes_zeros.get_prefix() + bytes_zeros.message)
        assert bytes_zeros.get_suffix(test_len) == expected
