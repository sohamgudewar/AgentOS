# # Authentication failure:
# File 1:

# {
#  "error": "Wrong password"
# }

# File 2:
# {
#  "error": "Invalid credentials"
# }

# File 3:
# {
#  "error": "Login failed"
# }
# Same problem, different responses.

# Solution: Custom Exceptions
# We created:
# app/core/exceptions.py
# with:

# class AgentOSError(Exception):
#     pass
# This is our base error.

# Then:
# class AuthenticationError(AgentOSError):
#     pass

# Meaning:
# "Authentication-related failures belong to this category."

class AgentOSError(Exception):
    """Base exception for AgentOS errors."""
    pass

class AuthenticationError(AgentOSError):
    """Exception raised for authentication errors."""
    pass

class AuthorizationError(AgentOSError):
    """Exception raised for authorization errors."""
    pass

class ResourceNotFoundError(AgentOSError):
    """Exception raised when a requested resource is not found."""
    pass

class ValidationError(AgentOSError):
    """Exception raised for validation errors."""
    pass

