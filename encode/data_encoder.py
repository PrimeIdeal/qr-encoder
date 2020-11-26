from abc import abstractmethod
from encode.common import ALPHANUMERIC_MAP, BLOCK_INFORMATION, CHAR_CAP, INDICATORS


class QREncoder:
    """
    QR Encoder object.
    """

    def __init__(self, message: str, correction_level: str) -> None:
        """
        Constructor for the qr_encoder class.

        Parameters
        ----------
        message : str
            The message to be encoded.
        correction_level : str
            Error correction level for the QR code.

        Raises
        ------
        ValueError
            Message is too long.
        """
        self.message = message
        self.correction_level = correction_level

        mode, msg_length = self.mode, len(message)

        for idx, cap in enumerate(CHAR_CAP[mode][correction_level]):
            if msg_length <= cap:
                self.version = idx + 1
                self.bit_cap = cap
                break
        else:
            raise ValueError(
                f'Message too long for correction level {correction_level}.'
            )

    def get_prefix(self) -> str:
        """
        Fetches mode and character count prefixes for the message.

        Returns
        -------
        str
            Concatenated prefixes.
        """
        mode = self.mode
        mode_prefix, indicator_lengths = INDICATORS[mode]

        if self.version < 10:
            char_prefix_length = indicator_lengths[0]
        elif self.version < 27:
            char_prefix_length = indicator_lengths[1]
        else:
            char_prefix_length = indicator_lengths[2]

        char_count = bin(len(self.message))[2:]
        char_count_prefix = _pad_bits(char_count, char_prefix_length)

        return mode_prefix + char_count_prefix

    def get_suffix(self, encoded_length: int) -> str:
        """
        Generates a suffix to extend the encoded message to its required
        length.

        The encoded message's required length depends on the encoder version
        and error correction level. To achieve the required length, a
        suffix of 0s is added if the length is not a multiple of 8, followed
        by repeating pad bytes.

        Parameters
        ----------
        encoded_length : int
            The length of the encoded message.

        Returns
        -------
        str
            The encoded message's suffix.
        """
        pass

    def get_num_bits(self):
        """
        Returns the required length of the encoded message based on encoder
        characteristics.

        Data codewords are 8 bits each.

        Returns
        -------
        int
            The required number of bits.
        """
        block_info = BLOCK_INFORMATION[self.version][self.correction_level]

        codeword_count = block_info[1]*block_info[2]
        if block_info[3]:
            codeword_count += block_info[3]*block_info[4]

        return 8*codeword_count

    @abstractmethod
    def encode(self) -> str:
        """Encodes self.message."""
        pass

    # TODO: More description here? Return type?
    def correct_error(self):
        pass

    @property
    def mode(self) -> str:
        return 'kanji'


class NumericEncoder(QREncoder):
    """
    QR Encoder using numeric encoding mode.
    """

    def encode(self) -> str:
        """
        Encodes the message in numeric mode.

        The message is split into 3-digit groups (the final group may have 1
        or 2 digits). Each group is converted to its binary representation and
        is left padded if necessary. The binary groups are then concatenated
        into the encoded string.

        Returns
        -------
        str
            Encoded message.
        """
        encoded_message = ''

        for i in range(0, len(self.message), 3):
            group = int(self.message[i:i+3])

            if group > 99:
                full_length = 10
            elif group > 9:
                full_length = 7
            else:
                full_length = 4

            bin_group = _pad_bits(bin(group)[2:], full_length)
            encoded_message += bin_group

        return encoded_message

    @property
    def mode(self) -> str:
        return 'numeric'


class AlphanumericEncoder(QREncoder):
    """
    QR Encoder using alphanumeric encoding mode.
    """

    def encode(self):
        """
        Encodes the message in alphanumeric mode.

        The message is split into 2-character groups. The first character of
        the group is mapped to an integer in [0, 44], multiplied by 45, then
        added to the integer representation of the second character. The sum
        is then converted to 11-bit binary (6 if the final group is only one
        character). The binary groups are then concatenated into the encoded
        string.

        Returns
        -------
        str
            Encoded message.
        """
        encoded_message = ''

        for i in range(0, len(self.message), 2):
            group = self.message[i: i + 2]

            first_char = int(
                group[0]) if group[0].isdecimal() else ALPHANUMERIC_MAP[
                group[0]]
            second_char = int(
                group[-1]) if group[-1].isdecimal() else ALPHANUMERIC_MAP[
                group[-1]]

            # TODO: Where is the 11 coming from? The 6 below?
            if len(group) == 2:
                bin_group = _pad_bits(
                    bin(45 * first_char + second_char)[2:], 11)
            else:
                bin_group = _pad_bits(bin(second_char)[2:], 6)

            encoded_message += bin_group
        return encoded_message

    @property
    def mode(self) -> str:
        return 'alphanumeric'


class BytesEncoder(QREncoder):
    """
    QR Encoder using bytes encoding mode.
    """

    def encode(self):
        """
        Encodes the message in bytes mode.

        Each character of the message is converted to a hexadecimal byte,
        which is then converted to an 8-bit binary string (left padded if
        necessary). The binary strings are then concatenated into the
        encoded message.

        Returns
        -------
        str
            Encoded message.
        """
        return ''.join(
            _pad_bits(bin(ord(char))[2:], 8) for char in self.message
        )

    @property
    def mode(self) -> str:
        return 'bytes'


def _pad_bits(
    bit_str: str,
    target_len: int,
    pad_from_left: bool = True
) -> str:
    """
    Helper function: pads bits to a specified length with 0s.

    Parameters
    ----------
    bit_str : str
        Binary number to be padded.
    target_len : int
        Desired length.
    pad_from_left : bool, optional
        Toggles padding from left or right (defaults to left).

    Returns
    -------
    str
        Padded string of bits. If the length of bit_str is greater than
        target_len, delete from the left or right according to pad_from_left.
    """

    skip_val = (-1) ** int(pad_from_left)
    return (bit_str[::skip_val] + '0' * target_len)[:target_len][::skip_val]
