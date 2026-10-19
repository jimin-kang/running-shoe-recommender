from pydantic import BaseModel
from shoe_recommender.schemas.shoe import ShoeResponse


class Recommendation(BaseModel):
    shoe: ShoeResponse
    score: float
    reasons: list[str]


class RecommendationResponse(BaseModel):
    recommendations: list[Recommendation]