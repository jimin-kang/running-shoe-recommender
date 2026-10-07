"""
Endpoint(s) for generating shoe recommendations.
"""

from typing import Optional

from fastapi import APIRouter, Depends, Request
from shoe_recommender.database.connection import get_db
from sqlalchemy.orm import Session

from shoe_recommender.schemas.preference import PreferenceRequest
from shoe_recommender.schemas.recommendation import RecommendationResponse
from shoe_recommender.services.recommendation_service import RecommendationService


router = APIRouter(
    prefix="/api/recommendations",
    tags=["recommendations"],
)

@router.post("", response_model=RecommendationResponse)
def get_recommendations(
    request: Request,
    preferences: PreferenceRequest,
    db: Session = Depends(get_db),
    limit: Optional[int] = None
):
    return request.app.state.recommendation_service.recommend(
        preferences=preferences, 
        db=db, 
        limit=limit
    )