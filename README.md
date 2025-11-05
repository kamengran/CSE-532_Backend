CSE-532 Backend — Game Recommendation API
This project is a **FastAPI-based backend** for a Game Recommendation System.  
It provides REST API endpoints for listing games and generating personalized recommendations based on content similarity.
 Features
- Built with **FastAPI** and **Uvicorn**
- Supports **filtering** by genre, platform, playtime, and rating
- Provides a **content-based recommender system**
- Includes `/docs` endpoint for interactive API testing (Swagger UI)
- Data is loaded from `data/games.csv`
-  Installation & Setup

### 1️ Clone the Repository
```bash
git clone https://github.com/kamengran/CSE-350_Backend.git
cd CSE-350_Backend
```

### 2️ Create and Activate Virtual Environment
**Windows:**
```bash
python -m venv .venv
.\.venv\Scripts\activate
```
**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3️ Install Dependencies
```bash
pip install fastapi uvicorn pandas scikit-learn numpy pydantic
```

### 4️ Run the Server
```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 5️ Open the API
Go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
to test the API endpoints in your browser.
