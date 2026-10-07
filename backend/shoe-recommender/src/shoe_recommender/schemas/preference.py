"""
Models for user shoe preferences.
"""

from typing import Optional

from pydantic import BaseModel, Field


class PreferenceRequest(BaseModel):
    weight: float = Field(..., description="Weight of the running shoe (g).")
    weight_importance: float = Field(
        ge=0,
        le=1,
    )
    
    forefoot_stack: float = Field(..., description="Forefoot stack height (mm).")
    forefoot_stack_importance: float = Field(
        ge=0,
        le=1,
    )
    
    heel_stack: float = Field(..., description="Heel stack height (mm).")
    heel_stack_importance: float = Field(
        ge=0,
        le=1,
    )
    
    plated: bool = Field(..., description="Whether the shoe is plated.")
    plated_constraint: bool = Field(..., description="Whether your plated preference is a dealbreaker.")

    # use_case: Optional[str] = Field(default=None, description="Desired use case for the running shoe (i.e. everyday, tempo, racing, trail, etc).")
    # cushioning: float = Field(
    #     ge=0,
    #     le=1,
    # )

    # responsiveness: float = Field(
    #     ge=0,
    #     le=1,
    # )

    # stiffness: float = Field(
    #     ge=0,
    #     le=1,
    # )

    # durability: float = Field(
    #     ge=0,
    #     le=1,
    # )