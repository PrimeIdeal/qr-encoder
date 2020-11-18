from encode.common import CHAR_CAP


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
        """
        self.message = message
        self.correction_level = correction_level

    def get_version(self) -> int:
        """
        Determines the smallest possible format for the QR code.

        Returns
        -------
        int
            QR format version.

        Raises
        ------
        ValueError
            Message is too long.
        """
        mode = self._get_mode()

        for idx, cap in enumerate(CHAR_CAP[mode][self.correction_level]):
            if len(self.message) <= cap:
                return idx+1

        raise ValueError(
            'Message is too long for specified error correction level.'
        )

    def get_num_bits(self):
        pass

    def preprocess(self):
        pass

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
