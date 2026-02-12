from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, PasswordChange
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hash d'un mot de passe avant stockage"""

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """vérifie que le mot de passe correspond au hash"""

    return pwd_context.verify(plain_password, hashed_password)


def create_user(db: Session, user_data: UserCreate):
    """Création d'un nouvel utilisateur"""

    # Vériication de l'email utilisateur à savoir si il existe déjà
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email déjà existant"
        )

    # Vérification de la présence du Username
    existing_username = (
        db.query(User).filter(User.username == user_data.username).first()
    )
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nom d'utilisateur déjà pris",
        )

    # Hash du mot de pass
    hashed_password = get_password_hash(user_data.password)

    # creation de l'objet utilisateur
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_user_by_email(db: Session, email: str):
    """Récupérer un utilisateur par email"""

    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    """Récupérer un utilisateur par ID"""

    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, user_id: int, updates: UserUpdate):
    """Met à jour un utilisateur"""

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    if updates.username:
        user.username = updates.username
    if updates.email:
        user.email = updates.email

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    """Supprime un utilisateur"""

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    db.delete(user)
    db.commit()
    return {"message": "Utilisateur supprimé"}


def change_password(db: Session, user_id: int, data: PasswordChange):
    """Modification du mot de passe d'un utilisateur connecté"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    # Vérifier que l'ancien mot de passe est correct
    if not verify_password(data.current_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Mot de passe actuel incorrect")
    # Vérifier que le nouveau mot de passe et la confirmation correspondent
    if data.new_password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Les mots de passe ne correspondent pas")
    # Hasher et sauvegarder le nouveau mot de passe
    user.hashed_password = get_password_hash(data.new_password)
    db.commit()
    db.refresh(user)
    return {"message": "Mot de passe modifié avec succès"}
