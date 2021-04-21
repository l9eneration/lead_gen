class EmailFinderError(Exception):
    """
    Generic exception class for the library
    """
    pass


class MissingCompanyError(EmailFinderError):
    pass


class MissingNameError(EmailFinderError):
    pass


class FinderApiError(EmailFinderError):
    """
    Represents something went wrong in the call to the Hunter API
    """
    pass