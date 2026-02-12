from pydantic import BaseModel, Field, constr
from typing import Optional
from app.models.exercise import BodyPart


"""Schemas pour les exercices (Exercise)
Définit les structures de données pour validation et réponse API.
"""


# ==========================================
# BASE
# ==========================================


class ExerciseBase(BaseModel):
    """Champs communs à tous les exos"""

    name: constr(min_length=3, max_length=100) = Field(
        ..., description="nom de l'exercice", examples=["pompes"]
    )
    body_part: BodyPart = Field(
        ..., description="Partie du corps ciblée (upper/core/lower)", examples=["upper"]
    )
    difficulty: int = Field(
        ..., ge=1, le=3, description="Niveau de difficulté (1 à 3)", examples=[2]
    )


# ==========================================
# CREATE
# ==========================================


class ExerciseCreate(ExerciseBase):
    """Création d'un nouvel exercice"""

    description: Optional[str] = Field(
        default=None, max_length=500, description="Description de l'exercice"
    )
    instructions: Optional[str] = Field(
        default=None, max_length=1000, description="Instructions détaillées"
    )
    reps: Optional[int] = Field(default=None, ge=1, description="Nombre de répétitions")
    duration_seconds: Optional[int] = Field(
        default=None, ge=1, description="Durée en secondes"
    )
    points_value: int = Field(..., ge=1, description="Points attribués à l'exercice")
    gif_url: Optional[str] = Field(
        default=None, max_length=255, description="URL du GIF d'animation"
    )


# ==========================================
# RESPONSE
# ==========================================


class ExerciseResponse(ExerciseBase):
    """Réponse API avec un exercice complet"""

    id: int
    description: Optional[str]
    instructions: Optional[str]
    reps: Optional[int]
    duration_seconds: Optional[int]
    points_value: int
    gif_url: Optional[str]

    class Config:
        from_attributes = True