from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import jwt
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer(auto_error=False)

class AuthMiddleware:
    """
    Authentication and authorization middleware
    """

    def __init__(self, secret_key: str = "your-secret-key-change-in-production"):
        self.secret_key = secret_key
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 60 * 24  # 24 hours

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT access token

        Args:
            data: Data to encode in the token
            expires_delta: Optional expiration time delta

        Returns:
            Encoded JWT token
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> dict:
        """
        Verify and decode a JWT token

        Args:
            token: JWT token to verify

        Returns:
            Decoded token payload

        Raises:
            HTTPException: If token is invalid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def get_current_user(self, credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> dict:
        """
        Get current user from JWT token

        Args:
            credentials: HTTP authorization credentials

        Returns:
            User information from token

        Raises:
            HTTPException: If authentication fails
        """
        if not credentials:
            # For now, allow anonymous access
            return {"user_id": "anonymous", "username": "anonymous"}

        try:
            payload = self.verify_token(credentials.credentials)
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return {"user_id": user_id, "username": payload.get("username", "user")}
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

# Create auth middleware instance
auth_middleware = AuthMiddleware()

# Dependency functions
def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> dict:
    """
    Dependency function to get current user
    """
    return auth_middleware.get_current_user(credentials)

def get_current_active_user(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Dependency function to get current active user
    """
    # In a real application, you would check if the user is active
    # For now, we'll just return the user
    return current_user

def require_auth(current_user: dict = Depends(get_current_active_user)) -> dict:
    """
    Dependency function that requires authentication
    """
    if current_user["user_id"] == "anonymous":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user

# Optional authentication (allows anonymous access)
def optional_auth(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> dict:
    """
    Optional authentication - allows anonymous access
    """
    if not credentials:
        return {"user_id": "anonymous", "username": "anonymous"}

    try:
        return auth_middleware.get_current_user(credentials)
    except HTTPException:
        # If token is invalid, fall back to anonymous
        return {"user_id": "anonymous", "username": "anonymous"}