## Running Shoe Recommender
### Overview
This is a web app that recommends running shoes.

### Requirements

### Startup
We need to start up both the backend and frontend servers.

Backend:
```
cd backend/shoe-recommender
uv run uvicorn shoe_recommender.main:app --reload
```

Frontend:
```
cd frontend/shoe-recommender
npm run dev
```
