"""
KKR Mind Exceptions - Custom error classes
"""


class KKRMindError(Exception):
    """Base exception for KKR Mind errors"""
    pass


class RateLimitError(KKRMindError):
    """Rate limit exceeded"""
    pass


class NetworkError(KKRMindError):
    """Network connection error"""
    pass


class InvalidResponseError(KKRMindError):
    """Invalid response from API"""
    pass


class ConfigurationError(KKRMindError):
    """Configuration error"""
    pass
