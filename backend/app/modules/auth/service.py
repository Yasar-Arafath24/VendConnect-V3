from sqlalchemy.orm import Session

from app.core.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.security import verify_password
from app.modules.auth.constants import INVALID_CREDENTIALS
from app.modules.auth.schema import (
    LoginRequest,
    TokenResponse,
)
from app.modules.users.repository import UserRepository


class AuthService:

    @staticmethod
    def login(
        db: Session,
        credentials: LoginRequest,
    ) -> TokenResponse:

        user = UserRepository.get_by_email(
            db,
            credentials.email,
        )

        if user is None:
            raise ValueError(INVALID_CREDENTIALS)

        if not verify_password(
            credentials.password,
            user.password_hash,
        ):
            raise ValueError(INVALID_CREDENTIALS)

        access_token = create_access_token(
            data={"sub": user.id}
        )

        refresh_token = create_refresh_token(
            data={"sub": user.id}
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    @staticmethod
    def refresh_access_token(
        refresh_token: str,
    ) -> TokenResponse:

        payload = decode_token(refresh_token)

        if payload is None:
            raise ValueError("Invalid refresh token.")

        if payload.get("type") != "refresh":
            raise ValueError("Invalid token type.")

        user_id = payload.get("sub")

        access_token = create_access_token(
            data={"sub": user_id}
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )