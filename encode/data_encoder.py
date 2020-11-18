class qr_encoder:

    def __init__(self, message: str, correction_level: str):
        self.message = message
        self.correction_level = correction_level

    def get_version(self):
        pass

    def get_num_bits(self):
        pass

    def preprocess(self):
        pass

    def postprocess(self):
        pass

    def correct_error(self):
        pass


class numeric_encoder(qr_encoder):

    def __init__(self, message: str, correction_level: str):
        qr_encoder.__init__(self, message, correction_level)

    def encode(self):
        pass


class alphanumeric_encoder(qr_encoder):

    def __init__(self, message: str, correction_level: str):
        qr_encoder.__init__(self, message, correction_level)

    def encode(self):
        pass


class bytes_encoder(qr_encoder):

    def __init__(self, message: str, correction_level: str):
        qr_encoder.__init__(self, message, correction_level)

    def encode(self):
        pass
