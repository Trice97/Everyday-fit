from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.workout import Workout, WorkoutExercise
from app.models.exercise import Exercise
from app.models.user import User
from app.schemas.workout import WorkoutComplete


"""Services pour la gestion des entraînements (workout)"""


# ==========================================
# CREATE
# ==========================================
def generate_workout(db: Session, user_id: int):
    """Generation automatique d'un training selon le niveau de difficulté selectionné par l'utilisateur"""

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    # selection d'exercice selon la difficulté selectionné par le user
    exercises = (
        db.query(Exercise)
        .filter(Exercise.difficulty == user.difficulty_level)
        .limit(3)
        .all()
    )

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
    return workout


# ==========================================
# COMPLETE
# ==========================================


def complete_workout(db: Session, workout_id: int, data: WorkoutComplete):
    """Marque un workout comme terminé"""

    workout = get_workout_by_id(db, workout_id)
    workout.is_completed = data.is_completed
    workout.total_points += 100
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
    
    total = len(workouts)
    completed = sum(1 for w in workouts if w.is_completed)
    pending = total - completed
    
    return {
        "workouts": workouts,
        "total": total,
        "completed": completed,
        "pending": pending
    }

