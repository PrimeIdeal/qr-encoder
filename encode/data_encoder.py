from encode.common import CHAR_CAP


class qr_encoder:

    def __init__(self, message: str, correction_level: str):
        self.message = message
        self.correction_level = correction_level

    def get_version(self):
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

    def _get_mode(self):
        return 'numeric'

    def encode(self):
        pass


class alphanumeric_encoder(qr_encoder):

    def _get_mode(self):
        return 'alphanumeric'

    def encode(self):
        pass


class bytes_encoder(qr_encoder):

    def _get_mode(self):
        return 'bytes'

    def encode(self):
        pass
