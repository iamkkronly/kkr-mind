"""
KKR Mind Configuration - API endpoints and settings

Developer: Kaustav Kanti Ray (@iamkkronly)
"""


class Config:
    """
    Configuration constants

    KKR Mind talks to a single private backend API.
    Backend details are abstracted away from users.
    """

    # Backend API endpoint
    API_BASE = "https://img-thumb-cache.iamkkronly58.workers.dev"
    CHAT_PATH = "/api"

    # Full chat endpoint, e.g.:
    #   GET {API_BASE}/api?chat=hello&system=optional%20persona
    CHAT_ENDPOINT = f"{API_BASE}{CHAT_PATH}"

    # Timeouts
    DEFAULT_TIMEOUT = 120

    # Rate limits (be gentle with the backend)
    MAX_REQUESTS_PER_MINUTE = 10

    # How many recent messages of client-side memory to send as context
    MEMORY_CONTEXT_MESSAGES = 10

    # User agent
    USER_AGENT = "KKRMind/1.0 (Python)"

    # Attribution
    DEVELOPER = "Kaustav Kanti Ray (@iamkkronly)"
