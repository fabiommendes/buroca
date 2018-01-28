class BurocaException(Exception):
    """
    Buroca errors.
    """


class TemplateError(BurocaException):
    """
    Error raised when a problem is found on a template
    """


class SkipViewer(BurocaException):
    """
    Raised to tell that a viewer should be skipped.
    """
