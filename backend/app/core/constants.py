# Today, we write:
# if user.role == "admin":
#     allow_access()

# Somewhere else:
# if role == "administrator":
#     ...

# Somewhere else:
# role = "Admin"

# Now we have three different values for the same thing.

# Problems:
# Typos
# Inconsistent naming
# Difficult changes
# Hard to maintain

# Example:

# ROLE_ADMN
# A small typo can break authorization.
# Solution: Centralized Constants
# We created:

"""
Application-wide constants.
"""
    
#API
API_V1_PREFIX = "/api/v1"

# User roles

ROLE_ADMIN = "admin"
ROLE_DEVELOPER = "developer"
ROLE_ANALYST = "analyst"
ROLE_VIEWER = "viewer"

ROLES= (
    ROLE_ADMIN,
    ROLE_DEVELOPER, 
    ROLE_ANALYST,
    ROLE_VIEWER,
)

# Agent Status

STATUS_ACTIVE = "active"
STATUS_INACTIVE = "inactive"
STATUS_DRAFT = "draft"

# Health 

HEALTH_OK = "healthy"

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100