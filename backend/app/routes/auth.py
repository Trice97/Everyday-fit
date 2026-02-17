from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.schemas.user import PasswordResetRequest, PasswordReset
from app.services.auth_service import create_access_token, verify_password, create_password_reset_token, verify_password_reset_token
from app.services.user_service import get_user_by_email, get_password_hash


router = APIRouter(prefix="/auth", tags=["Authentication"])



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


# =========================================
# PASSWORD RESET
# =========================================
@router.post("/forgot-password")
def forgot_password(data: PasswordResetRequest, db: Session = Depends(get_db)):
    """Génère un token de réinitialisation de mot de passe"""
    user = get_user_by_email(db, data.email)
    if not user:
        # On retourne toujours success pour ne pas révéler si l'email existe
        return {"message": "Si l'email existe, un token a été généré"}
    
    token = create_password_reset_token(data.email)
    # En prod, on enverrait le token par email
    # Ici on le retourne directement (pour tester)
    return {
        "message": "Token généré avec succès",
        "token": token  # À retirer en prod
    }

@router.post("/reset-password")
def reset_password(data: PasswordReset, db: Session = Depends(get_db)):
    """Réinitialise le mot de passe avec un token"""
    email = verify_password_reset_token(data.token)
    user = get_user_by_email(db, email)
    
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    if data.new_password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Les mots de passe ne correspondent pas")
    
    user.hashed_password = get_password_hash(data.new_password)
    db.commit()
    
    return {"message": "Mot de passe réinitialisé avec succès"}