# Récap de toutes les modifications de la session

---

## BACKEND

### 1. `backend/app/services/workout_service.py`
**Problème :** Les workouts étaient toujours identiques.
**Modifications :**
- Ajout de l'import `from sqlalchemy.sql import func` et `from app.models.exercise import Exercise, BodyPart`
- Refonte de la fonction `generate_workout` :
  - Avant : prenait 3 exercices au hasard tous body parts confondus avec `.limit(3)` → toujours les mêmes
  - Après : pioche **1 exercice UPPER + 1 CORE + 1 LOWER** via une fonction `pick(body_part)` avec `.order_by(func.random()).first()`

---

### 2. `backend/app/routes/users.py`
**Ajout :** Nouvelle route `PUT /users/me/level` pour sauvegarder le niveau après le test.
- Import ajouté : `from app.models.user import User, DifficultyLevel`
- Nouveau modèle Pydantic `LevelUpdate` (champ `difficulty_level: int`)
- Nouvel endpoint qui met à jour `current_user.difficulty_level` en DB

---

### 3. `backend/seed_exercises.py`
**Nouveau fichier** (remplace l'ancien vide).
- 36 exercices répartis : 4 par body part (UPPER / CORE / LOWER) × 3 niveaux (1/2/3)
- Ne duplique pas les exercices déjà présents (vérifie par nom)
- **Pour l'utiliser :**
  ```bash
  cd backend
  source venv/bin/activate
  python seed_exercises.py
  ```

---

## FRONTEND

### 4. `frontend/index.html`
**Refonte complète** — ancienne page avec hero/bienfaits/how-it-works supprimée.
- Splash screen plein écran avec "Everyday**Fit**" centré
- Clic n'importe où → transition vers `intro.html`
- Couleurs : noir pur + rouge `#CC0000`
- Police : Impact pour le titre
- Suppression du lien vers `css/style.css`
- Ajout balises no-cache

---

### 5. `frontend/intro.html`
**Nouveau fichier** créé de zéro.
- Texte de présentation avec **effet typewriter** (lettre par lettre)
- Texte modifiable dans la variable `TEXT` ligne ~100
- Vitesse modifiable via `SPEED` (ms par lettre)
- Deux boutons après le texte :
  - "Je veux me prendre en main" → `login.html`
  - "Non merci je n'aime pas le sport" → lance la vidéo Papa Swolio
- **Overlay vidéo plein écran** : mettre le fichier dans `frontend/videos/papa-swolio.mp4`
- **Clic n'importe où** sur la page → redirige vers `login.html`
- Suppression du lien vers `css/style.css`
- Ajout balises no-cache

---

### 6. `frontend/login.html`
**Refonte complète** — ancienne page avec choix motivé/flemme supprimée.
- Design minimaliste noir/rouge
- **Deux onglets** : Connexion / Créer un compte
- Connexion : email + mot de passe → appelle `POST /api/auth/login`
  - Si test de niveau jamais fait → redirige vers `level-test.html`
  - Sinon → redirige vers `dashboard.html`
- Inscription : username + email + password → appelle `POST /api/users/`
  - Connexion automatique après inscription → redirige vers `level-test.html`
- Ajout balises no-cache

---

### 7. `frontend/level-test.html`
**Nouveau fichier** créé de zéro.
- 4 questions avec barre de progression
- Calcul automatique du niveau selon le score total :
  - Score 0-2 → Débutant (1)
  - Score 3-5 → Intermédiaire (2)
  - Score 6-8 → Avancé (3)
- Sauvegarde le niveau via `PUT /api/users/me/level`
- Stocke `level_done_{userId}` dans le `localStorage` pour ne pas repasser le test à chaque connexion
- Affiche le niveau obtenu + bouton vers `dashboard.html`

---

### 8. `frontend/dashboard.html`
**Refonte complète** — ancienne page supprimée.
- Design minimaliste noir/rouge
- Affiche le **badge de niveau** (DEBUTANT / INTERMEDIAIRE / AVANCE)
- Stats compactes : points, workouts complétés, taux de réussite
- **Carrousel éditions** redesigné
- Bouton "Générer mon workout" → appelle `POST /api/workouts/generate`
- Historique accordéon
- Lien "Refaire le test →" sur le badge de niveau

---

### 9. `frontend/workout.html`
**Refonte complète** — ancienne page supprimée.
- Design minimaliste noir/rouge
- **Slot machine** : bordure rouge `#CC0000` (était jaune `#fbbf24`)
- Messages du slot en rouge uppercase
- **Bouton "↺ Nouveau workout"** dans la navbar → regénère un workout et recharge
- Timings du slot ajustés : rouleaux s'arrêtent à 3s / 5.5s / 7.5s (total ~9s)
- Bouton "Workout terminé" sobre sans `alert()`
- 3 zones d'exercices (UPPER / CORE / LOWER) dans l'ordre de la DB

---

### 10. `frontend/css/style.css`
**Non modifié mais inutilisé** — toutes les nouvelles pages utilisent des styles inline (`<style>` dans le `<head>`). Ce fichier peut être supprimé sans impact.

---

## FICHIERS DE RÉFÉRENCE

### 11. `CHARTE_GRAPHIQUE.md`
**Nouveau fichier** — document de référence avec :
- Tableau de toutes les couleurs et leur rôle
- Tableau de remplacement (ancienne couleur → nouvelle)
- Règles de style (navbar, cards, boutons)
- Liste des pages redesignées

---

## RÉSUMÉ DES COULEURS (charte actuelle)

| Rôle | Couleur |
|------|---------|
| Background général | `#0a0a0a` |
| Cards / sections | `#111111` |
| Bordures | `#1e1e1e` |
| Accent principal | `#CC0000` (rouge) |
| Texte principal | `#ffffff` |
| Texte secondaire | `#444444` |
| Succès (exercice complété) | `#22c55e` |

---

## FLOW UTILISATEUR COMPLET

```
index.html        → splash, clic pour entrer
    ↓
intro.html        → présentation typewriter + 2 boutons
    ↓
login.html        → connexion OU inscription
    ↓
level-test.html   → 4 questions → niveau calculé et sauvegardé en DB
    ↓
dashboard.html    → badge niveau + stats + générer workout
    ↓
workout.html      → slot machine + 3 exercices (UPPER/CORE/LOWER)
```
