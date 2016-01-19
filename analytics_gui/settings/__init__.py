from .base import *  # NOQA
try:
    from .local import *  # NOQA
except ImportError:
    import warnings
    warnings.warn('No local settings module found.')
