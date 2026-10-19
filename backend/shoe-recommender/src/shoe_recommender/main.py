from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from shoe_recommender.database.connection import SessionLocal, create_database
from shoe_recommender.api.shoes import router as shoes_router
from shoe_recommender.api.recommendations import router as recommendations_router
from shoe_recommender.database.load_stats import load_shoe_stats
from shoe_recommender.database.seed import seed_database
from shoe_recommender.services.recommender import RecommendationService

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle tasks that need to occur upon application startup and shutdown.
    
    Upon startup, we need to create our database schema, load shoe catalog stats, and create our recommendation service.

    Args:
        app (FastAPI): application instance
    """
    create_database()
    seed_database()
    with SessionLocal() as session:
        shoe_stats = load_shoe_stats(session=session)
    app.state.recommender = RecommendationService(shoe_stats=shoe_stats)
    
    yield
    
    # Do any cleanup here

# Create the app
app = FastAPI(
    title="Running Shoe Recommender",
    lifespan=lifespan,
)

# Add CORS middleware: required to accept requests from our frontend
origins = [
    f"http://localhost:5173",  # Default Vite port
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all HTTP headers
)

# Expose the shoe & recommendation routes
app.include_router(shoes_router)
app.include_router(recommendations_router)