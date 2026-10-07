"""
Models for shoes.

Defines information that each shoe should have and what must be exchanged in API requests.
"""
from pydantic import BaseModel


class ShoeResponse(BaseModel):
    id: int
    brand: str
    model: str

    weight_g: float | None
    heel_stack_mm: float | None
    forefoot_stack_mm: float | None
    drop_mm: float | None

    use_case: str | None
    terrain: str | None