from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.modules.auth.dependencies import get_current_user
from app.modules.users.schema import UserResponse
from app.modules.users.model import User
from app.database.session import get_db
from app.modules.auth.schema import RefreshTokenRequest
from app.modules.auth.schema import (
    LoginRequest,
    TokenResponse,
)
from app.modules.auth.service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db),
):
    try:
        return AuthService.login(
            db,
            credentials,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )
        
@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user

@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh_token(
    request: RefreshTokenRequest,
):
    try:
        return AuthService.refresh_access_token(
            request.refresh_token,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )