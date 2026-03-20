"""Script pour completer la DB avec des exercices variés.
   3 body parts x 3 niveaux x ~4 exercices = ~36 exercices au total.
   Lance avec : python seed_exercises.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal
from app.models.workout import Workout, WorkoutExercise
from app.models.exercise import Exercise, BodyPart
from app.models.user import User

EXERCISES = [
    # ==============================
    # UPPER — Niveau 1 (Débutant)
    # ==============================
    {"name": "Push-up Débutant",        "body_part": BodyPart.UPPER, "difficulty": 1, "reps": 10, "description": "Pompes classiques sur les genoux, parfaites pour débuter."},
    {"name": "Wall Push-up",            "body_part": BodyPart.UPPER, "difficulty": 1, "reps": 12, "description": "Pompes debout contre un mur. Idéal pour les grands débutants."},
    {"name": "Shoulder Tap",            "body_part": BodyPart.UPPER, "difficulty": 1, "reps": 16, "description": "En position planche, touche alternativement chaque épaule."},
    {"name": "Incline Push-up",         "body_part": BodyPart.UPPER, "difficulty": 1, "reps": 10, "description": "Pompes mains sur une surface surélevée (table, canapé). Plus facile que les pompes normales."},

    # ==============================
    # UPPER — Niveau 2 (Intermédiaire)
    # ==============================
    {"name": "Push-up Standard",        "body_part": BodyPart.UPPER, "difficulty": 2, "reps": 15, "description": "Pompes classiques au sol, corps bien droit de la tête aux talons."},
    {"name": "Wide Push-up",            "body_part": BodyPart.UPPER, "difficulty": 2, "reps": 12, "description": "Pompes mains écartées pour cibler les pectoraux."},
    {"name": "Diamond Push-up",         "body_part": BodyPart.UPPER, "difficulty": 2, "reps": 10, "description": "Pompes mains en losange, cible l'intérieur des pecs et les triceps."},
    {"name": "Pike Push-up",            "body_part": BodyPart.UPPER, "difficulty": 2, "reps": 10, "description": "Pompes en V inversé pour travailler les épaules."},
    
    # ==============================
    # UPPER — Niveau 3 (Avancé)
    # ==============================
    {"name": "Archer Push-up",          "body_part": BodyPart.UPPER, "difficulty": 3, "reps": 8,  "description": "Pompes asymétriques — une bras tendu sur le côté, l'autre fléchi. Très exigeant."},
    {"name": "Chest Tap Push-up",       "body_part": BodyPart.UPPER, "difficulty": 3, "reps": 8,  "description": "Pompe explosive, tu te frappes la poitrine au point haut."},
    {"name": "Clap Push-up",            "body_part": BodyPart.UPPER, "difficulty": 3, "reps": 6,  "description": "Pompe pliométrique avec applaudissement en l'air. Force et explosivité."},
    {"name": "Decline Push-up",         "body_part": BodyPart.UPPER, "difficulty": 3, "reps": 10, "description": "Pieds surélevés sur une chaise, cible le haut des pectoraux."},

    # ==============================
    # CORE — Niveau 1 (Débutant)
    # ==============================
    {"name": "Crunch Basique",          "body_part": BodyPart.CORE, "difficulty": 1, "reps": 15, "description": "Abdominaux classiques en remontant doucement le buste."},
    {"name": "Planche Genoux",          "body_part": BodyPart.CORE, "difficulty": 1, "duration_seconds": 30, "description": "Planche sur les genoux. Maintiens le dos bien droit."},
    {"name": "Toucher de Chevilles",    "body_part": BodyPart.CORE, "difficulty": 1, "reps": 20, "description": "Allongé, tu touches alternativement tes chevilles en contractant les obliques."},
    {"name": "Relevé de Jambes Léger",  "body_part": BodyPart.CORE, "difficulty": 1, "reps": 12, "description": "Allongé sur le dos, tu montes les genoux fléchis vers la poitrine."},

    # ==============================
    # CORE — Niveau 2 (Intermédiaire)
    # ==============================    
    {"name": "Planche Classique",       "body_part": BodyPart.CORE, "difficulty": 2, "duration_seconds": 45, "description": "Gainage face au sol sur les avant-bras. Corps rigide comme une planche."},
    {"name": "Russian Twist",           "body_part": BodyPart.CORE, "difficulty": 2, "reps": 20, "description": "Assis, pieds décollés, tu tournes le buste de gauche à droite."},
    {"name": "Bicycle Crunch",          "body_part": BodyPart.CORE, "difficulty": 2, "reps": 20, "description": "Crunch en pédalant — coude gauche vers genou droit, et vice versa."},
    {"name": "Dead Bug",                "body_part": BodyPart.CORE, "difficulty": 2, "reps": 12, "description": "Allongé sur le dos, bras vers le plafond, tu étends un bras et la jambe opposée en alternance."},

    # ==============================
    # CORE — Niveau 3 (Avancé)
    # ==============================
    {"name": "Planche Latérale",        "body_part": BodyPart.CORE, "difficulty": 3, "duration_seconds": 40, "description": "Gainage latéral sur un avant-bras. Hanche bien relevée."},
    {"name": "Dragon Flag",             "body_part": BodyPart.CORE, "difficulty": 3, "reps": 6,  "description": "Exercice de Bruce Lee — corps tendu, tu descends lentement depuis la verticale."},
    {"name": "Crunch Frog",             "body_part": BodyPart.CORE, "difficulty": 3, "reps": 12, "description": "Crunch jambes fléchies en grenouille. Très intense pour les abdos."},
    {"name": "L-Sit Partiel",           "body_part": BodyPart.CORE, "difficulty": 3, "duration_seconds": 20, "description": "Assis au sol, mains à plat, tu essaies de soulever ton bassin en tendant les jambes."},

    # ==============================
    # LOWER — Niveau 1 (Débutant)
    # ==============================
    {"name": "Squat Débutant",          "body_part": BodyPart.LOWER, "difficulty": 1, "reps": 15, "description": "Squat sans charge, dos droit, descend jusqu'à ce que les cuisses soient parallèles au sol."},
    {"name": "Fente Statique",          "body_part": BodyPart.LOWER, "difficulty": 1, "reps": 12, "description": "Fente avant, tu restes en position basse quelques secondes avant de remonter."},
    {"name": "Glute Bridge",            "body_part": BodyPart.LOWER, "difficulty": 1, "reps": 15, "description": "Allongé sur le dos, pieds au sol, tu pousses le bassin vers le plafond."},
    {"name": "Step-up Imaginaire",      "body_part": BodyPart.LOWER, "difficulty": 1, "reps": 20, "description": "Simulation de montée de marche sur place. Genoux hauts."},

    # ==============================
    # LOWER — Niveau 2 (Intermédiaire)
    # ==============================
    {"name": "Squat Sauté",             "body_part": BodyPart.LOWER, "difficulty": 2, "reps": 12, "description": "Squat classique suivi d'un saut explosif. Atterris souple."},
    {"name": "Fente Marchée",           "body_part": BodyPart.LOWER, "difficulty": 2, "reps": 16, "description": "Fentes en avançant sur 8 pas dans chaque direction."},
    {"name": "Frog Jumps",              "body_part": BodyPart.LOWER, "difficulty": 2, "reps": 10, "description": "Squat profond puis saut explosif vers l'avant comme une grenouille."},
    {"name": "Single Leg Glute Bridge", "body_part": BodyPart.LOWER, "difficulty": 2, "reps": 12, "description": "Glute bridge sur une seule jambe. Maintiens le bassin bien aligné."},

    # ==============================
    # LOWER — Niveau 3 (Avancé)
    # ==============================
    {"name": "Pistol Squat",            "body_part": BodyPart.LOWER, "difficulty": 3, "reps": 6,  "description": "Squat sur une jambe, l'autre tendue devant. Équilibre et force maximale."},
    {"name": "Jumping Lunge",           "body_part": BodyPart.LOWER, "difficulty": 3, "reps": 12, "description": "Fentes sautées en alternant les jambes dans les airs."},
    {"name": "Box Jump",                "body_part": BodyPart.LOWER, "difficulty": 3, "reps": 8,  "description": "Sauter sur une surface surélevée (chaise, canapé), atterrir accroupi."},
    {"name": "Bulgarian Split Squat",   "body_part": BodyPart.LOWER, "difficulty": 3, "reps": 10, "description": "Fente avec le pied arrière surélevé sur une chaise. Très exigeant pour les quadriceps."},
]
def seed():
    db = SessionLocal()
    added = 0
    skipped = 0

    for data in EXERCISES:
        exists = db.query(Exercise).filter(Exercise.name == data["name"]).first()
        if exists:
            skipped += 1
            continue

        ex = Exercise(
            name=data["name"],
            body_part=data["body_part"],
            difficulty=data["difficulty"],
            reps=data.get("reps"),
            duration_seconds=data.get("duration_seconds"),
            description=data.get("description", ""),
            points_value=10,
        )
        db.add(ex)
        added += 1

    db.commit()
    db.close()
    print(f"✅ Seed terminé — {added} exercices ajoutés, {skipped} déjà présents.")


if __name__ == "__main__":
    seed()