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
                'Message is too long for specified error correction level.'
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
        pad_length = char_prefix_length - len(char_count)

        char_count_prefix = pad_length*'0' + char_count

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

    def encode(self):
        pass


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
