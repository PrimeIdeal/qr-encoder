from encode.common import (
    CHAR_CAP,
    INDICATORS
)


class qr_encoder:
    """
    QR Encoder object.
    """

    def __init__(self, message: str, correction_level: str):
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

        mode, msg_length = self._get_mode(), len(message)

        for idx, cap in enumerate(CHAR_CAP[mode][correction_level]):
            if msg_length <= cap:
                self.version = idx+1
                self.bit_cap = cap
                break
        else:
            raise ValueError(
                f'Message too long for correction level {correction_level}.'
            )

    def preprocess(self) -> str:
        """
        Fetches mode and character count prefixes for the message.

        Returns
        -------
        str
            Concatenated prefixes.
        """
        mode = self._get_mode()
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

    def postprocess(self):
        pass

    def correct_error(self):
        pass

    def _get_mode(self):
        return 'kanji'


class numeric_encoder(qr_encoder):
    """
    QR Encoder using numeric encoding mode.
    """

    def _get_mode(self):
        return 'numeric'

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
        encoded_msg = ''

        for i in range(0, len(self.message), 3):
            group = int(self.message[i:i+3])

            if group > 99:
                pad_length = 10
            elif group > 9:
                pad_length = 7
            else:
                pad_length = 4

            bin_group = _pad_bits(bin(group)[2:], pad_length)
            encoded_msg += bin_group

        return encoded_msg


class alphanumeric_encoder(qr_encoder):
    """
    QR Encoder using alphanumeric encoding mode.
    """

    def _get_mode(self):
        return 'alphanumeric'

    def encode(self):
        pass


class bytes_encoder(qr_encoder):
    """
    QR Encoder using bytes encoding mode.
    """

    def _get_mode(self):
        return 'bytes'

    def encode(self):
        pass


def _pad_bits(bits: str, target_len: int, left: bool = True) -> str:
    """
    Helper function: pads bits to a specified length with 0s.

    Parameters
    ----------
    bits : str
        Binary number to be padded.
    target_len : int
        Desired length.
    left : bool, optional
        Toggles padding from left or right (defaults to left).

    Returns
    -------
    str
        Padded string of bits.
    """
    pad_length = target_len - len(bits)

    padded = pad_length*'0' + bits if left else bits + pad_length*'0'

    return padded
