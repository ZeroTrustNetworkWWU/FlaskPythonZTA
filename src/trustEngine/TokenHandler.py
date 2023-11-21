# a class for providing session tokens

class TokenHandler:
    def __init__(self):
        self.tokenIndex = 0

    def getNewToken(self):
        self.tokenIndex += 1
        return self.tokenIndex