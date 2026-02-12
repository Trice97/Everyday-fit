from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.schemas.exercise import ExerciseResponse


"""Schemas pour les entraînements (Workout)
Définit les structures de données pour validation et réponse API.
"""

# ==========================================
# WORKOUT EXERCISE (exercice dans un workout)
# ==========================================


class WorkoutExerciseResponse(BaseModel):
    """Un exercise dans un entraînement"""

    order: int = Field(..., description="ordre de l'exercise dans le workout")
    exercise: ExerciseResponse
    target_reps: Optional[int] = Field(None, description="Objectif de répitions")
    target_duration: Optional[int] = Field(None, description="Objectif de durée en seconde")

    class Config:
        from_attributes = True


# ==========================================
# CREATE
# ==========================================


class WorkoutCreate(BaseModel):
    """Génération d'un nouveau workout"""

    # Pas besoin de paramètres pour la création :
    # le backend génère selon le niveau de l'utilisateur
    pass


# class WorkoutCreate(BaseModel):
#    body_part_focus: Optional[BodyPart] = None  # Si le user veut cibler une zone
#    duration_preference: Optional[int] = None   # Durée souhaitée en minutes


# ==========================================
# COMPLETE
# ==========================================


class WorkoutComplete(BaseModel):
    """Validation d'un workout comme étant terminé"""

    is_completed: bool = Field(
        True, description="marque le training comme étant terminé"
    )


# ==========================================
# RESPONSE
# ==========================================


class WorkoutResponse(BaseModel):
    """réponse API avec un workout complet"""

    id: int
    user_id: int
    difficulty_level: int
    total_points: int
    is_completed: bool
    created_at: datetime
    exercises: List[WorkoutExerciseResponse] = []

    class Config:
        from_attributes = True