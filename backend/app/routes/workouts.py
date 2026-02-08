from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.workout import WorkoutResponse, WorkoutComplete
from app.services import workout_service


router = APIRouter(prefix="/workouts", tags=["Workouts"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================================
# CREATE - Génération automatique d’un workout
# ==========================================
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