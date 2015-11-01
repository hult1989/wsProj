class AppException(Exception):
    pass


class NoUserException(AppException):
    def __init__(self, args=None):
        super(Exception, self).__init__(args)
        self.errCode = 401


class NoImeiException(AppException):
    def __init__(self, args=None):
        super(Exception, self).__init__(args)
        self.errCode = 403

class NoSubException(AppException):
    def __init__(self, args=None):
        super(Exception, self).__init__(args)
        self.errCode = 405
