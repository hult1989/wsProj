class AppException(Exception):
    pass

class InvalidFormatException(AppException):
    def __init__(self, args=None):
        super(Exception, self).__init__(args)
        self.errCode = 300

class DuplicateUsernameException(AppException):
    def __init__(self, args=None):
        super(Exception, self).__init__(args)
        self.errCode = 400

class NoUserException(AppException):
    def __init__(self, args=None):
        super(Exception, self).__init__(args)
        self.errCode = 401

class PasswordErrorException(AppException):
    def __init__(self, args=None):
        super(Exception, self).__init__(args)
        self.errCode = 402

class NoImeiException(AppException):
    def __init__(self, args=None):
        super(Exception, self).__init__(args)
        self.errCode = 403

class NoSubException(AppException):
    def __init__(self, args=None):
        super(Exception, self).__init__(args)
        self.errCode = 405

class NoBindException(AppException):
    def __init__(self, args=None):
        super(Exception, self).__init__(args)
        self.errCode = 404

class NoStickAckException(AppException):
    def __init__(self, args=None):
        super(Exception, self).__init__(args)
        self.errCode = 501

class DuplicateSosnumberException(AppException):
    def __init__(self, args=None):
        super(Exception, self).__init__(args)
        self.errCode = 502

class NoSosnumberException(AppException):
    def __init__(self, args=None):
        super(Exception, self).__init__(args)
        self.errCode = 503

class NoMoreDataException(AppException):
    def __init__(self, args=None):
        super(Exception, self).__init__(args)
        self.errCode = 504

class SimnumChangedException(AppException):
    def __init__(self, args=None):
        super(Exception, self).__init__(args)
        self.errCode = 505

class StorageLimitException(AppException):
    def __init__(self, args=None):
        super(Exception, self).__init__(args)
        self.errCode = 507

class SosMinimumException(AppException):
    def __init__(self, args=None):
        super(Exception, self).__init__(args)
        self.errCode = 508

