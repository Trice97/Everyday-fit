from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.database import Base


class DifficultyLevel(enum.IntEnum):
    """Niveau de difficulté attribué après un test de détermination de niveau"""

    DEBUTANT = 1
    INTERMEDIAIRE = 2
    AVANCE = 3


class User(Base):
    """Table des utilisateurs de Fitness Clash"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # Niveau de difficulté par défaut : Débutant
    difficulty_level = Column(
        Enum(DifficultyLevel), default=DifficultyLevel.DEBUTANT, nullable=False
    )

    total_points = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relation avec les workouts (sera définie dans workout.py)
    workouts = relationship("Workout", back_populates="user")

    def __repr__(self):
        return f"<User(username={self.username}, level={self.difficulty_level.name})>"