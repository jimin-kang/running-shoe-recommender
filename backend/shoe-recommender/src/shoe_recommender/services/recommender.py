from dataclasses import asdict
import json
from typing import Optional
from fastapi import Request
from shoe_recommender.database.models.shoe_stats import ShoeFeatureStats

from sqlalchemy import select
from sqlalchemy.orm import Session

from shoe_recommender.database.models.shoe import Shoe
from shoe_recommender.schemas.preference import PreferenceRequest
from shoe_recommender.schemas.recommendation import (
    Recommendation,
    RecommendationResponse,
)
from shoe_recommender.schemas.shoe import ShoeResponse


class RecommendationService:
    """
    Service that generates shoe recommendations.
    """

    def __init__(self, shoe_stats: ShoeFeatureStats):
        """
        Our recomender needs shoe catalog statistics to compute shoe scores.

        Args:
            shoe_stats (ShoeFeatureStats): shoe catalog statistics
        """
        self.shoe_stats = shoe_stats # shoe stats required to normalize features

    def recommend(
        self,
        preferences: PreferenceRequest,
        db: Session,
        limit: Optional[int] = None,
    ) -> RecommendationResponse:
        
        # filter shoes by hard constraints
        shoes = self._get_candidate_shoes(preferences=preferences, db=db)

        # rank the eligible shoes
        recommendations = [
            self._score_shoe(shoe, preferences)
            for shoe in shoes
        ]

        # return them (highest score first)
        recommendations.sort(
            key=lambda recommendation: recommendation.score,
            reverse=True,
        )
        return RecommendationResponse(
            recommendations=recommendations[:limit] if limit else recommendations
        )
        

    def _get_candidate_shoes(
        self,
        preferences: PreferenceRequest,
        db: Session
    ) -> list[Shoe]:
        """
        Filter out shoes based on user specified constraints.
        
        I.e. weight < 10 oz, 30 mm < stack < 40 mm, etc.  

        Args:
            preferences (PreferenceRequest): _description_
            db (Session): _description_

        Returns:
            list[Shoe]: _description_
        """
        # TODO: implement
        statement = select(Shoe)

        # Basic filtering for now
        # if preferences.plated_constraint:
        #     statement = statement.where(
        #         Shoe.plated == preferences.plated
        #     )

        return list(db.scalars(statement).all())


    def _score_shoe(
        self,
        shoe: Shoe,
        preferences: PreferenceRequest,
    ) -> Recommendation:
        """
        Generate a score for the shoe based on the User's preference.
        
        The shoe's score will be between 0 & 1, where higher scores indicate a better match for the user.

        Args:
            shoe (Shoe): shoe to score
            preferences (PreferenceRequest): user's shoe preferences

        Returns:
            Recommendation: the recommendation object containing the shoe score
        """
        # The score of a shoe will be inversely proportional to the distance between the user's shoe preferences & the shoe.
        # I.e. shoes closer to the user's preference vector will be scored higher (indicating a better match).
        
        # Compute weighted Manhattan distance between the shoe & user preferences.
        # Features are on z-scores to normalize the scale (i.e. 30g weight delta should not necessarily overpower a 3mm stack delta).
        shoe_weight_z = (shoe.weight_g - self.shoe_stats.weight.mean) / self.shoe_stats.weight.std
        pref_weight_z = (preferences.weight - self.shoe_stats.weight.mean) / self.shoe_stats.weight.std
        
        forefoot_stack_z = (shoe.forefoot_stack_mm - self.shoe_stats.forefoot_stack.mean) / self.shoe_stats.forefoot_stack.std
        pref_forefoot_stack_z = (preferences.forefoot_stack - self.shoe_stats.forefoot_stack.mean) / self.shoe_stats.forefoot_stack.std
        
        heel_stack_z = (shoe.heel_stack_mm - self.shoe_stats.heel_stack.mean) / self.shoe_stats.heel_stack.std
        pref_heel_stack_z = (preferences.heel_stack - self.shoe_stats.heel_stack.mean) / self.shoe_stats.heel_stack.std
        
        distance = (
            preferences.weight_importance
            * abs(shoe_weight_z - pref_weight_z)

            + preferences.forefoot_stack_importance
            * abs(forefoot_stack_z - pref_forefoot_stack_z)

            + preferences.heel_stack_importance
            * abs(heel_stack_z - pref_heel_stack_z)
        )
        
        # Similarity score will be computed using reciprocal distance similarity (https://www.puttypeg.net/book/chapters/chapter4.html).
        # Scores will be bounded between 0 & 1, where a score of 1 indicates a perfect match for the user.
        similarity_score = 1/(1 + distance)

        return Recommendation(
            shoe=ShoeResponse(
                id=shoe.id,
                brand=shoe.brand.name,
                model=shoe.model,
                weight_g=shoe.weight_g,
                heel_stack_mm=shoe.heel_stack_mm,
                forefoot_stack_mm=shoe.forefoot_stack_mm,
                drop_mm=shoe.drop_mm,
                use_case=shoe.use_case,
                terrain=shoe.terrain,
            ),
            score=similarity_score,
            reasons=[], # TODO: extract these
        )
        
        
def get_recommender(request: Request) -> RecommendationService:
    """
    Dependency injector to yield the Recommendation Service.

    Args:
        request (Request): incoming request

    Returns:
        RecommendationService: application RecommendationService instance
    """
    return request.app.state.recommender