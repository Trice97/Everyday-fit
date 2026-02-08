from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError

from app.database import SessionLocal
from app.models.user import User
from app.services.auth_service import decode_access_token


# =========================================
# Sécurité HTTP Bearer
# =========================================
security = HTTPBearer()


# =========================================
# Dépendance DB
# =========================================
def get_db():
    """ouvre une session DB pour chaque requête"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================
# dependance utilisateur courant
# =========================================
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    Verifie le token JWT envoyé par le client et renvoie l'utilisateur correspondant
    """
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="token invalide (pas d'identifiant utilisateur)",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user_id = int(user_id_str)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Format de token invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé",
        )

    return user