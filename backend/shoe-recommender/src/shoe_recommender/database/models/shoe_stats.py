from dataclasses import dataclass


@dataclass
class FeatureStats:
    """
    Stats to compute for each shoe feature used in the recommendation score.
    """
    mean: float
    std: float
    min: float
    max: float


@dataclass
class ShoeFeatureStats:
    """
    Shoe features to compute stats for.
    
    These features will be used when computing recommendation scores.
    """
    weight: FeatureStats
    forefoot_stack: FeatureStats
    heel_stack: FeatureStats