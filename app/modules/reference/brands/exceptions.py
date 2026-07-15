class BrandError(Exception):
    """Base exception for Brand module."""


class BrandNotFoundError(BrandError):
    """Raised when a brand is not found."""


class BrandNameAlreadyExistsError(BrandError):
    """Raised when a brand name already exists."""


class BrandCodeAlreadyExistsError(BrandError):
    """Raised when a brand code already exists."""