class HunterIOError(Exception):
    """
    Generic exception class for the library
    """
    pass


class MissingCompanyError(HunterIOError):
    pass


class MissingNameError(HunterIOError):
    pass


class HunterApiError(HunterIOError):
    """
    Represents something went wrong in the call to the Hunter API
    """
    pass