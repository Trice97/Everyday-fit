from sqlalchemy import Column, Integer, String, Enum, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base
import enum
from sqlalchemy.orm import relationship


class BodyPart(str, enum.Enum):
    """Parties du corps ciblées par l'exercice"""

    UPPER = "UPPER"
    CORE = "CORE"
    LOWER = "LOWER"


class Exercise(Base):
    """Table des exercices bodyweight"""

    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    body_part = Column(Enum(BodyPart), nullable=False, index=True)
    difficulty = Column(Integer, nullable=False, index=True)

    description = Column(Text, nullable=True)
    instructions = Column(Text, nullable=True)

    reps = Column(Integer, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    points_value = Column(Integer, nullable=False, default=10)
    gif_url = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relation avec la table intermédiair Workoutexercise
    workout_exercises = relationship(
        "WorkoutExercise",
        back_populates="exercise",
        lazy="select",
        overlaps="exercise"
    )

    def __repr__(self):
        return f"<Exercise(name={self.name}, part={self.body_part}, level={self.difficulty})>"
