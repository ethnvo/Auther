# AuthHer 🧠✨

**AuthHer** is a search engine for academic papers that prioritizes research authored by women.  
Our goal is to amplify women-led scholarship by ranking papers with women authors higher in search results.

> Built with 💻 Next.js + Django | Designed in Figma | Created for VenusHacks 2025

---

## 🔍 Features

- Search academic papers (MVP uses sample dataset)
- Automatically tags and ranks papers based on author gender
- Clean UI built with Tailwind CSS
- Gender inference using [genderize.io](https://genderize.io/)

---

## 🧱 Tech Stack

| Layer      | Tech                              |
| ---------- | --------------------------------- |
| Frontend   | Next.js, TypeScript, Tailwind CSS |
| Backend    | Django, Django REST Framework     |
| Database   | SQLite (MVP)                      |
| Gender API | genderize.io                      |

---

## ⚙️ Local Setup

### 🧰 Run the Project Locally

```bash
# --- Frontend (Next.js) ---
cd authher-frontend
npm install
npm run dev
# Open http://localhost:3000

# --- Backend (Django) ---
cd ../backend
python3 -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
pip install -r requirements.txt

# Run Django server
python manage.py migrate
python manage.py runserver
# Open http://localhost:8000/api/papers/
```
