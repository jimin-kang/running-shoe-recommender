from dataclasses import asdict
import json
from typing import Optional
from shoe_recommender.database.models.shoe_stats import ShoeFeatureStats
from shoe_recommender.recommendation.vectorizer import weighted_cosine_similarity

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
    Service that provides shoe recommendations.
    
    Calculating recommendation scores should be abstracted away here.
    This should just orchestrate shoe filtering & ranking.
    """

    def __init__(self, shoe_stats: ShoeFeatureStats):
        self.shoe_stats = shoe_stats # shoe stats required to normalize features
        print(f"LOADED SHOE STATS:\n{json.dumps(asdict(self.shoe_stats), indent=2)}")

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
        
        Higher score indicates a better match for the user.

        Args:
            shoe (Shoe): _description_
            preferences (PreferenceRequest): _description_

        Returns:
            Recommendation: _description_
        """
        # Compute weighted distance between shoe vector & user preferences
        # Features are on z-scores to normalize the scale 
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
        similarity_score = 1/(1 + distance)
        print(f"User pref vs. shoe '{shoe.model}' -> Weighted Similarity = {similarity_score:.4f}")

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
            reasons=[],
        )