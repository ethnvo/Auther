# auther

**auther** is a search engine for academic papers that prioritizes research authored by women.  
Our goal is to amplify women-led scholarship by ranking papers with women authors higher in search results.

> Built with 💻 Next.js + Django | Designed in Figma | Created for VenusHacks 2025

### 🌐 Live Demo: [Try it here](https://auther-yifd.vercel.app/)

### 🧠 Backend API: [https://auther-rdxl.onrender.com/api/papers/?search=soccer](https://auther-rdxl.onrender.com/api/papers/?search=soccer)
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
| Database   |  PostGresQL                       |
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
# Open http://localhost:3000
```
---

### ⚠️ Known Issues / Limitations
Overly broad searches (e.g., "art") may not return results properly due to result overload or timeouts.

Favorited results are partially implemented on the backend but not yet available in the UI (excluded due to deadline constraints).

Search filters (e.g., After 2022 or Fully Authored by Women) are partially implemented (in the API, not implemented in frontend) and may produce incomplete results and/or extended load times.

Some searches may appear to fail by showing blank results prematurely if the backend response is delayed.

Failed searches may return nothing for up to 1 hour due to caching behavior.

Author-based searches may be incomplete if the author appears under multiple name variations (e.g., Ethan Vo vs. Ethan K. Vo), leading to inconsistent tagging.
