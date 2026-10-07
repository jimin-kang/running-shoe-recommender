"""
Endpoints for fetching shoes.
May need this to populate shoe options and/or allow user to select shoes.
"""
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
):
    """
    Get all shoes.

    Args:
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        _type_: _description_
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
):
    """
    Get a particular shoe.

    Args:
        shoe_id (int): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
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