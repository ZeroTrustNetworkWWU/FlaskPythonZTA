class MissingTrustData(Exception):
    def __init__(self, message):
        super().__init__(message)

class LowTrustLevel(Exception):
    def __init__(self, message):
        super().__init__(message)