from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.services import user_service
from app.dependencies.auth import get_current_user
from app.models.user import User, DifficultyLevel
from app.schemas.user import UserCreate, UserResponse, UserUpdate, PasswordChange, UserStats
from pydantic import BaseModel

class LevelUpdate(BaseModel):
    difficulty_level: int  # 1, 2 ou 3


router = APIRouter(prefix="/users", tags=["Users"])


# ==========================================
# CREATE - Register
# ==========================================
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user_data)

# ==========================================
# USER STATS
# ==========================================
@router.get("/me/stats", response_model=UserStats)
def get_my_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Récupère les statistiques de l'utilisateur connecté"""
    return user_service.get_user_stats(db, current_user.id)


# ==========================================
# UPDATE LEVEL - Après le test de niveau
# ==========================================
@router.put("/me/level")
def update_my_level(
    data: LevelUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Sauvegarde le niveau déterminé par le test"""
    if data.difficulty_level not in [1, 2, 3]:
        raise HTTPException(status_code=400, detail="Niveau invalide (1, 2 ou 3)")
    current_user.difficulty_level = DifficultyLevel(data.difficulty_level)
    db.commit()
    db.refresh(current_user)
    return {"difficulty_level": current_user.difficulty_level}


# ==========================================
# READ - Get user by ID
# ==========================================
@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="utilisateur introuvable")
    return user


# ==========================================
# UPDATE
# ==========================================
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updates: UserUpdate, db: Session = Depends(get_db)):
    return user_service.update_user(db, user_id, updates)


# =============================================
# DELETE
# =============================================
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.delete_user(db, user_id)


# ==========================================
# CHANGE PASSWORD
# ==========================================
@router.put("/me/password")
def change_password(
    data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Modification du mot de passe de l'utilisateur connecté"""
    return user_service.change_password(db, current_user.id, data)

