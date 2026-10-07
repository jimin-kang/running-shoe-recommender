from fastapi import Depends
from shoe_recommender.database.models.shoe import Shoe
from sqlalchemy import func, select
from sqlalchemy.orm import InstrumentedAttribute, Session

from shoe_recommender.database.connection import get_db
from shoe_recommender.database.models.shoe_stats import FeatureStats, ShoeFeatureStats


def load_shoe_stats(session: Session) -> ShoeFeatureStats:
    """
    Load shoe feature stats required to normalize each feature when computing recommendation scores.

    Returns:
        ShoeFeatureStats: _description_
    """
    weight_stats = load_feature_stats(
        session=session,
        feature=Shoe.weight_g
    )
    forefoot_stack_stats = load_feature_stats(
        session=session,
        feature=Shoe.forefoot_stack_mm
    )
    heel_stack_stats = load_feature_stats(
        session=session,
        feature=Shoe.heel_stack_mm
    )
    return ShoeFeatureStats(
        weight=weight_stats,
        forefoot_stack=forefoot_stack_stats,
        heel_stack=heel_stack_stats
    )


def load_feature_stats(session: Session, feature: InstrumentedAttribute[float]) -> FeatureStats:
    """
    Load the feature stats required to normalize the feature (i.e. min, max, mean, stddev).
    Will be used when computing similarity scores between user preference & shoes.

    Args:
        feature (InstrumentedAttribute[float]): _description_

    Returns:
        FeatureStats: _description_
    """
    # define query to get stats
    stmt = select(
        func.min(feature).label("min"),
        func.max(feature).label("max"),
        func.avg(feature).label("mean"),
        # func.stddev(feature).label("std"),
    )
    result = session.execute(stmt).one()
    
    # compute stddev (SQLite doesn't support stddev natively)
    stddev_stmt = select(
        func.sqrt(
            func.avg(feature * feature) - func.pow(func.avg(feature), 2)
        )
    )
    stddev_result = session.execute(stddev_stmt).scalar_one()

    # return the FeatureStats object
    return FeatureStats(
        mean=result.mean,
        min=result.min,
        max=result.max,
        std=stddev_result,
    )