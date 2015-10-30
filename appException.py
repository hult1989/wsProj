class NoUserException(Exception):
    def __init__(self):
        self.errCode = 401


class NoImeiException(Exception):
    def __init__(self):
        self.errCode = 403

class NoSubException(Exception):
    def __init__(self):
        self.errCode = 405
