from pydantic import BaseModel, EmailStr, Field, constr
from typing import Optional
from datetime import datetime

"""Schemas pour les utilisateurs (User)
Définit les structures de données pour validation et réponse API.
"""


# ==========================================
# BASE
# ==========================================


class UserBase(BaseModel):
    """Champs communs"""

    username: constr(min_length=3, max_length=50) = Field(
        ..., description="Nom d'utilisateur", examples=["tricepa"]
    )
    email: EmailStr = Field(
        ..., description="Adresse email valide", examples=["tricepa@fit.com"]
    )


# ==========================================
# CREATE
# ==========================================


class UserCreate(UserBase):
    """Création d'un utilisateur"""

    password: constr(min_length=8, max_length=20) = Field(
        ...,
        description="Mot de passe de 8 à 20 à caractères",
        examples=["monpasse123"],
    )


# ==========================================
# UPDATE
# ==========================================


class UserUpdate(BaseModel):
    """Modification d'un utilisateur"""

    username: Optional[constr(min_length=3, max_length=50)] = None
    email: Optional[EmailStr] = None


# ==========================================
# RESPONSE
# ==========================================


class UserResponse(UserBase):
    """Réponse API avec un utilisateur complet"""

    id: int
    total_points: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ==========================================
# LOGIN & TOKEN
# ==========================================


class UserLogin(BaseModel):
    """Connexion utilisateur"""

    email: EmailStr
    password: str


# ==========================================
# PASSWORD CHANGE
# ==========================================


class PasswordChange(BaseModel):
    """Modification du mot de passe d'un utilisateur connecté"""
    current_password: str = Field(
        ..., description="Mot de passe actuel"
    )
    new_password: constr(min_length=8, max_length=20) = Field(
        ..., description="Nouveau mot de passe (8 à 20 caractères)"
    )
    confirm_password: str = Field(
        ..., description="Confirmation du nouveau mot de passe"
    )


# ==========================================
# USER STATS
# ==========================================
class UserStats(BaseModel):
    """Statiques d'un utilisateur"""
    username: str
    total_points: int
    total_workouts: int
    completed_workouts: int
    completion_rate: float
    
    class Config:
        from_attributes = True
    