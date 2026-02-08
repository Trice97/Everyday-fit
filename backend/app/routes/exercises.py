from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.exercise import ExerciseCreate, ExerciseResponse
from app.services import exercise_service


router = APIRouter(prefix="/exercises", tags=["Exercises"])


# ==========================================
# DÉPENDANCE DB
# ==========================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================================
# CREATE - Ajouter un exercice
# ==========================================
@router.post("/", response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
def create_exercise_route(exercise_data: ExerciseCreate, db: Session = Depends(get_db)):
    """Creer un nouvel exercice"""
    return exercise_service.create_exercise(db, exercise_data)


# ==========================================
# READ - Récupérer un exercice par ID
# ==========================================
@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    """récuperer un exercise specifique"""
    exercise = exercise_service.get_exercise_by_id(db, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercice introuvable")
    return exercise


# ==========================================
# READ - Lister tous les exercices
# ==========================================
@router.get("/", response_model=list[ExerciseResponse])
def list_exercises(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """lister tous les exercices"""
    return exercise_service.get_all_exercises(db, skip=skip, limit=limit)


# ==========================================
# UPDATE - Modifier un exercice
# ==========================================
@router.put("/{exercise_id}", response_model=ExerciseResponse)
def update_exercise(
    exercise_id: int, updates: ExerciseCreate, db: Session = Depends(get_db)
):
    """ "met à jour un exercise"""
    return exercise_service.update_exercise(db, exercise_id, updates)


# ==========================================
# DELETE - Supprimer un exercice
# ==========================================
@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    """Supprime un exercise"""
    return exercise_service.delete_exercise(db, exercise_id)