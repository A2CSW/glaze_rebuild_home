from __future__ import annotations
class GlazeError(Exception):
    """Base exception for the GLAZE application."""
class DataLoadError(GlazeError):
    """Raised when data cannot be loaded safely."""
class DataSaveError(GlazeError):
    """Raised when data cannot be saved safely."""
class SchemaValidationError(GlazeError):
    """Raised when a DataFrame does not match the required schema."""
class RecordValidationError(GlazeError):
    """Raised when one or more records fail validation rules."""
class ServiceError(GlazeError):
    """Raised when a domain service operation fails."""
