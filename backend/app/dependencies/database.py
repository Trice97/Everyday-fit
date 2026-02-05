
from app.database import SessionLocal

def get_db():
	"""Dependance pour obtenir une session DB, Ouvre une session, 
	la fournie à la route puis la ferme automatiquement une l'action terminée"""

	db = SessionLocal()

	try:
		yield db 
	finally:
		db.close()
