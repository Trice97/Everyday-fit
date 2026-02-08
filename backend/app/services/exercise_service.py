from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.exercise import Exercise
from app.schemas.exercise import ExerciseCreate


"""Services pour la gestion des exercises"""


# ==========================================
# CREATE
# ==========================================
def create_exercise(db: Session, exercise_data: ExerciseCreate):
    """fonction pour créer un nouvel exercise"""

    existing_exercise = (
        db.query(Exercise).filter(Exercise.name == exercise_data.name).first()
    )
    if existing_exercise:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un exercise avec ce nom existe déjà",
        )

    # creation du nouvel exercise
    new_exercise = Exercise(**exercise_data.model_dump())
    db.add(new_exercise)
    db.commit()
    db.refresh(new_exercise)
    return new_exercise


# ==========================================
# READ
# ==========================================
def get_exercise_by_id(db: Session, exercise_id: int):
    """ "Récupère un exercise par ID"""
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="exercise introuvable")
    return exercise


def get_all_exercises(db: Session, skip: int = 0, limit: int = 20):
    """récupère la liste de tous les exercises (pagination possible)"""
    return db.query(Exercise).offset(skip).limit(limit).all()


# ==========================================
# UPDATE
# ==========================================


def update_exercise(db: Session, exercise_id: int, updates: ExerciseCreate):
    """mise à jour d'exercise"""
    exercise = get_exercise_by_id(db, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise introuvable")

    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(exercise, key, value)

    db.commit()
    db.refresh(exercise)
    return exercise


# ==========================================
# DELETE
# ==========================================


def delete_exercise(db: Session, exercise_id: int):
    """supprime un exercise"""
    exercise = get_exercise_by_id(db, exercise_id)
    db.delete(exercise)
    db.commit()
    return {"message": "Exercice supprimé avec succès"}
