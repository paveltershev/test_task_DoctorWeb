class FileStorageException(Exception):
    pass

class FileNotFoundError(FileStorageException):
    pass

class FileNotOwnedException(FileStorageException):
    pass

class AuthenticationError(FileStorageException):
    pass