"""
Converts shoes to vectors.

Shoe
 ↓
[0.31, 0.68, 0.56, ...]
"""

from typing import List

import numpy as np
from shoe_recommender.database.models.shoe import Shoe

class ShoeVectorizer:
    """
    Convert a Shoe into a Vector.
    """

    def transform(
        self,
        shoe: Shoe
    ) -> List[float]:
        return [
            shoe.weight_g,
            shoe.heel_stack_mm,
            shoe.forefoot_stack_mm
        ]


def weighted_cosine_similarity(user_vector: List[float], shoe_vector: List[float], weights: List[float]) -> float:
    """
    Compute the weighted cosine similarity between a user's preference vector and a shoe vector.
    """
    u = np.asarray(user_vector, dtype=float)
    i = np.asarray(shoe_vector, dtype=float)
    w = np.asarray(weights, dtype=float)
    
    # Dot product of weighted vectors
    numerator = np.sum(w * u * i)
    
    # Magnitudes of weighted vectors
    denominator = np.sqrt(np.sum(w * (u ** 2))) * np.sqrt(np.sum(w * (i ** 2)))
    
    if denominator == 0:
        return 0.0
        
    return float(numerator / denominator)