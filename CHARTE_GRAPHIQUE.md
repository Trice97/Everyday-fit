# Charte graphique Everyday Fit

## Couleurs

| Rôle              | Valeur      | Usage                                      |
|-------------------|-------------|-------------------------------------------|
| Rouge principal   | `#CC0000`   | Boutons CTA, accents, logo, slot machine  |
| Rouge hover       | `#EE0000`   | Survol des boutons rouges                 |
| Rouge sombre      | `#330000`   | Bordures subtiles sur fond noir           |
| Noir pur          | `#000000`   | Navbar, overlay                           |
| Noir principal    | `#0a0a0a`   | Background général des pages              |
| Noir card         | `#111111`   | Cards, formulaires, sections              |
| Noir élevé        | `#1a1a1a`   | Fond des formulaires (form-card)          |
| Bordure subtile   | `#1e1e1e`   | Borders de cards et inputs                |
| Bordure visible   | `#2a2a2a`   | Inputs focus off, séparateurs             |
| Blanc             | `#ffffff`   | Texte principal                           |
| Gris clair        | `#bbbbbb`   | Texte secondaire                          |
| Gris moyen        | `#666666`   | Labels, placeholders                      |
| Gris foncé        | `#444444`   | Texte désactivé, dates                    |
| Gris très foncé   | `#333333`   | Texte quasi invisible                     |
| Vert succès       | `#22c55e`   | Exercice complété, validation             |
| Vert hover        | `#16a34a`   | Hover bouton vert                         |

---

## Typographie

- **Titres / Logo** : `Impact, 'Arial Black', sans-serif` — tout en majuscules, letter-spacing 0.04–0.1em
- **Sous-titres / Labels** : `Arial, sans-serif` — uppercase, letter-spacing 0.08–0.15em, petit (0.7–0.85rem)
- **Corps de texte** : `Arial, sans-serif` — normal, color `#444` à `#bbb` selon importance

---

## Règles de style

- **Fond global** : `#0a0a0a` (pas de blanc, pas de bleu)
- **Navbar** : `background: #000`, `border-bottom: 2px solid #1a1a1a`
- **Cards** : `background: #111`, `border: 1px solid #1e1e1e`, `border-radius: 5–6px`
- **Bouton principal** : `background: #CC0000`, `border-radius: 4px`, texte blanc uppercase
- **Bordure active** : `border-color: #CC0000` (slot machine, card active, input focus)
- **Pas de box-shadow colorée** sauf rouge : `rgba(204,0,0,0.2–0.5)`
- **Zéro bleu** (`#60a5fa`, `#2563eb`, etc.) — remplacer partout par rouge ou blanc

---

## Pour modifier une page manuellement

Si une page a encore l'ancien design (bleu/slate), voici les remplacements à faire :

### Dans le CSS ou les styles inline :

```
#111827  →  #0a0a0a   (background body)
#1e293b  →  #111111   (background sections)
#334155  →  #1a1a1a   (background cards)
#475569  →  #1e1e1e   (bordures)
#0f172a  →  #000000   (navbar / footer)

#60a5fa  →  #CC0000   (accent principal)
#2563eb  →  #CC0000   (navbar background → mettre #000)
#1e40af  →  #1a1a1a   (navbar border → mettre 2px solid #1a1a1a)

#10b981  →  #22c55e   (vert succès — valeur très proche, ok de garder)
#064e3b  →  #0d1f0d   (fond vert foncé complété)

#94a3b8  →  #444444   (texte gris secondaire)
#cbd5e1  →  #bbbbbb   (texte gris clair)
#fbbf24  →  #CC0000   (jaune slot machine → rouge)
```

### Dans les balises HTML :
- Supprimer les classes `navbar`, `btn-primary`, `hero`, etc. de l'ancien style.css
- Les nouvelles pages utilisent des **styles inline** (balise `<style>` dans le `<head>`)
- Pas besoin du fichier `css/style.css` pour les nouvelles pages

---

## Pages déjà redesignées ✅

- `index.html` — splash screen
- `intro.html` — présentation + typewriter
- `login.html` — connexion / inscription
- `level-test.html` — test de niveau
- `dashboard.html` — tableau de bord
- `workout.html` — séance d'entraînement

## Fichier à ne plus toucher

`css/style.css` — ancien fichier, conservé mais inutilisé par les nouvelles pages.
