from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.services.auth_service import create_access_token, verify_password
from app.dependencies.auth import get_current_user


router = APIRouter(prefix="/auth", tags=["Authentication"])


# =========================================
# Dépendance DB
# =========================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================
# LOGIN (connexion utilisateur)
# =========================================
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Authentifie l'utilisateur et renvoie un token JWT
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


# =========================================
# ME (utilisateur courant)
# =========================================
@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    """
    renvoie les informationsde l'utilisateur connecté.
    nécessite un token JWT valide dans le header Authorization.
    """
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "difficulty_level": current_user.difficulty_level,
        "total_points": current_user.total_points,
    }