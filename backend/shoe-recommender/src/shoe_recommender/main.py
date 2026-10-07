"""
Application entrypoint: 
- Startup the FastAPI server
- Create the database schema 
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from shoe_recommender.database.connection import SessionLocal, create_database
from shoe_recommender.api.shoes import router as shoes_router
from shoe_recommender.api.recommendations import router as recommendations_router
from shoe_recommender.database.load_stats import load_shoe_stats
from shoe_recommender.database.seed import seed_database
from shoe_recommender.services.recommendation_service import RecommendationService

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    seed_database()
    with SessionLocal() as session:
        shoe_stats = load_shoe_stats(session=session)
    app.state.recommendation_service = RecommendationService(shoe_stats=shoe_stats)
    yield


app = FastAPI(lifespan=lifespan)

app = FastAPI(
    title="Running Shoe Recommender",
    lifespan=lifespan,
)

# Add CORS middleware to the app to allow requests from the following sources
# TODO: configure these ports
origins = [
    # "http://localhost:3000",  # Default Create React App port
    f"http://localhost:5173",  # Default Vite port
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all HTTP headers
)

app.include_router(shoes_router)
app.include_router(recommendations_router)