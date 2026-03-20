import random
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.workout import Workout, WorkoutExercise
from app.models.exercise import Exercise, BodyPart
from app.models.user import User
from app.schemas.workout import WorkoutComplete


"""Services pour la gestion des entraînements (workout)"""


# ==========================================
# CREATE
# ==========================================
def generate_workout(db: Session, user_id: int):
    """Generation automatique d'un training selon le niveau de difficulté selectionné par l'utilisateur.
    Slot 1 = UPPER  |  Slot 2 = CORE  |  Slot 3 = LOWER  — chacun random."""

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    def pick(body_part):
        candidates = (
            db.query(Exercise)
            .filter(
                Exercise.difficulty == user.difficulty_level,
                Exercise.body_part == body_part,
            )
            .all()
        )
        return random.choice(candidates) if candidates else None

    upper = pick(BodyPart.UPPER)
    core  = pick(BodyPart.CORE)
    lower = pick(BodyPart.LOWER)

    exercises = [ex for ex in [upper, core, lower] if ex is not None]

    if not exercises:
        raise HTTPException(status_code=404, detail="Aucun exercice trouvé")

    # création du workout
    new_workout = Workout(
        user_id=user.id,
        difficulty_level=user.difficulty_level,
        total_points=0,
        is_completed=False,
    )
    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)

    # creation des liens WorkoutExercise
    for index, ex in enumerate(exercises, start=1):
        link = WorkoutExercise(
            workout_id=new_workout.id,
            exercise_id=ex.id,
            order=index,
            target_reps=10,
            target_duration=None,
        )
        db.add(link)

    db.commit()

# Récupère les WorkoutExercise associés au workout
    workout_exercises = (
        db.query(WorkoutExercise)
        .filter(WorkoutExercise.workout_id == new_workout.id)
        .all()
    )

    # Charge les exercices liés pour chaque WorkoutExercise
    for w_ex in workout_exercises:
        _ = w_ex.exercise  # force SQLAlchemy à charger la relation

    new_workout.exercises = workout_exercises

    db.refresh(new_workout)

    return new_workout


# ==========================================
# READ
# ==========================================
def get_workout_by_id(db: Session, workout_id: int):
    """recupere un workout par son ID"""

    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout introuvable")

    for w_ex in workout.workout_exercises:
        _ = w_ex.exercise  # force SQLAlchemy à charger la relation

    workout.exercises = workout.workout_exercises
    return workout


# ==========================================
# COMPLETE
# ==========================================


def complete_workout(db: Session, workout_id: int):
    """Marque un workout comme terminé"""
    workout = get_workout_by_id(db, workout_id)
    workout.is_completed = True
    workout.total_points = 100
    
    # Ajouter les points au user
    user = db.query(User).filter(User.id == workout.user_id).first()
    user.total_points += 100
    
    db.commit()
    db.refresh(workout)
    return workout


# ==========================================
# DELETE
# ==========================================


def delete_workout(db: Session, workout_id: int):
    """Supprime un workout et ses exercises associés"""

    workout = get_workout_by_id(db, workout_id)
    db.delete(workout)
    db.commit()
    return {"message": "Workout supprimé avec succès"}

# ==========================================
# WORKOUT HISTORY
# ==========================================
def get_user_workout_history(db: Session, user_id: int, completed_only: bool = False):
    """Récupère l'historique des workouts d'un utilisateur"""
    query = db.query(Workout).filter(Workout.user_id == user_id)
    
    if completed_only:
        query = query.filter(Workout.is_completed == True)
    
    workouts = query.order_by(Workout.created_at.desc()).all()

    for workout in workouts:
        for w_ex in workout.workout_exercises:
            _ = w_ex.exercise
        workout.exercises = workout.workout_exercises

    total = len(workouts)
    completed = sum(1 for w in workouts if w.is_completed)
    pending = total - completed
    
    return {
        "workouts": workouts,
        "total": total,
        "completed": completed,
        "pending": pending
    }