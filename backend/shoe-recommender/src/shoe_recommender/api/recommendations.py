from typing import Optional

from fastapi import APIRouter, Depends, Request
from shoe_recommender.database.connection import get_db
from sqlalchemy.orm import Session

from shoe_recommender.schemas.preference import PreferenceRequest
from shoe_recommender.schemas.recommendation import RecommendationResponse
from shoe_recommender.services.recommender import RecommendationService, get_recommender


router = APIRouter(
    prefix="/api/recommendations",
    tags=["recommendations"],
)

@router.post("", response_model=RecommendationResponse)
def get_recommendations(
    preferences: PreferenceRequest,
    recommender: RecommendationService = Depends(get_recommender),
    db: Session = Depends(get_db),
    limit: Optional[int] = None
) -> RecommendationResponse:
    """
    Generate shoe recommendations based on the user's preferences.
    
    Args:
        preferences (PreferenceRequest): user's shoe preferences
        recommender (RecommendationService): recommendation service to generate shoe recs 
        db (Session, optional): database session scoped to the incoming request. Defaults to Depends(get_db).
        limit (Optional[int], optional): limit on the number of recommendations to return. Defaults to None.

    Returns:
        RecommendationResponse: list of shoe recommendations
    """
    return recommender.recommend(
        preferences=preferences, 
        db=db, 
        limit=limit
    )