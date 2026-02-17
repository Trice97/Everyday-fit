from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services import workout_service
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.workout import WorkoutResponse, WorkoutComplete, WorkoutHistory

router = APIRouter(prefix="/workouts", tags=["Workouts"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =============================================
# CREATE - Génération automatique d’un workout
# ===========================================
@router.post("/generate/{user_id}", response_model=WorkoutResponse)
def generate_workout(user_id: int, db: Session = Depends(get_db)):
    """genere un nouvelk entrainemenr pour l'utilisateur"""

    return workout_service.generate_workout(db, user_id)


# ==========================================
# READ - Récupérer un workout par ID
# ==========================================
@router.get("/{workout_id}", response_model=WorkoutResponse)
def get_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = workout_service.get_workout_by_id(db, workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout introuvable")
    return workout


# ==========================================
# UPDATE - Marquer un workout comme complété
# ==========================================
@router.put("/{workout_id}/complete", response_model=WorkoutResponse)
def complete_workout(
    workout_id: int, data: WorkoutComplete, db: Session = Depends(get_db)
):
    return workout_service.complete_workout(db, workout_id, data)


# ==========================================
# DELETE
# ==========================================
@router.delete("/{workout_id}", status_code=204)
def delete_workout(workout_id: int, db: Session = Depends(get_db)):
    return workout_service.delete_workout(db, workout_id)

# ==========================================
# WORKOUT HISTORY
# ==========================================
@router.get("/me/history", response_model=WorkoutHistory)
def get_my_workout_history(
    completed_only: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Récupère l'historique des workouts de l'utilisateur connecté"""
    return workout_service.get_user_workout_history(db, current_user.id, completed_only)