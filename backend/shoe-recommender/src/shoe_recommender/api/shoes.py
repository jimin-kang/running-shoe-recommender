from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from shoe_recommender.database.connection import get_db
from shoe_recommender.database.models.shoe import Shoe
from shoe_recommender.schemas.shoe import ShoeResponse


router = APIRouter(prefix="/api/shoes", tags=["shoes"])


@router.get("", response_model=list[ShoeResponse])
def get_shoes(
    db: Session = Depends(get_db),
) -> List[ShoeResponse]:
    """
    Get all shoes.
    
    Args:
        db (Session, optional): database session scoped to the request. Defaults to Depends(get_db).
    
    Returns:
        List[ShoeResponse]: list of all shoes
    """
    shoes = db.scalars(
        select(Shoe)
    ).all()

    return [
        ShoeResponse(
            id=shoe.id,
            brand=shoe.brand.name,
            model=shoe.model,
            weight_g=shoe.weight_g,
            heel_stack_mm=shoe.heel_stack_mm,
            forefoot_stack_mm=shoe.forefoot_stack_mm,
            drop_mm=shoe.drop_mm,
            use_case=shoe.use_case,
            terrain=shoe.terrain,
        )
        for shoe in shoes
    ]
    
@router.get("/{shoe_id}", response_model=ShoeResponse)
def get_shoe(
    shoe_id: int,
    db: Session = Depends(get_db),
) -> ShoeResponse:
    """
    Get a particular shoe.

    Args:
        shoe_id (int): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_

    Returns:
        ShoeResponse: shoe object
    """
    shoe = db.get(Shoe, shoe_id)

    if shoe is None:
        raise HTTPException(
            status_code=404,
            detail="Shoe not found",
        )

    return ShoeResponse(
        id=shoe.id,
        brand=shoe.brand.name,
        model=shoe.model,
        weight_g=shoe.weight_g,
        heel_stack_mm=shoe.heel_stack_mm,
        forefoot_stack_mm=shoe.forefoot_stack_mm,
        drop_mm=shoe.drop_mm,
        use_case=shoe.use_case,
        terrain=shoe.terrain,
    )