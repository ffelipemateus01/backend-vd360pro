from serial import SerialException
from psycopg2 import DatabaseError

class SivecError(SerialException):
    pass

class SivecIndexError(IndexError):
    pass

class SivecRepositoryError(SystemError):
    pass

class OtoError(SerialException):
    pass

class OtoIndexError(IndexError):
    pass

class PatientDbError(DatabaseError):
    pass

class PatientNotFound(DatabaseError):
    pass