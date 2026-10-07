"""
Populate the shoe database with real data.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from shoe_recommender.database.connection import SessionLocal
from shoe_recommender.database.models import Brand, Shoe


BRANDS = [
    "ASICS",
    "HOKA",
    "Saucony",
    "adidas",
    "Nike",
    "Brooks",
    "New Balance",
]


SHOES = [
    {
        "brand": "ASICS",
        "model": "Novablast 5",
        "weight_g": 255,
        "heel_stack_mm": 42,
        "forefoot_stack_mm": 34,
        "drop_mm": 8,
        "use_case": "daily",
        "terrain": "road",
    },
    {
        "brand": "ASICS",
        "model": "Superblast 2",
        "weight_g": 249,
        "heel_stack_mm": 45,
        "forefoot_stack_mm": 37,
        "drop_mm": 8,
        "use_case": "daily",
        "terrain": "road",
    },
    {
        "brand": "HOKA",
        "model": "Clifton 10",
        "weight_g": 278,
        "heel_stack_mm": 42,
        "forefoot_stack_mm": 34,
        "drop_mm": 8,
        "use_case": "daily",
        "terrain": "road",
    },
    {
        "brand": "HOKA",
        "model": "Mach 6",
        "weight_g": 232,
        "heel_stack_mm": 37,
        "forefoot_stack_mm": 32,
        "drop_mm": 5,
        "use_case": "tempo",
        "terrain": "road",
    },
    {
        "brand": "Saucony",
        "model": "Endorphin Speed 5",
        "weight_g": 237,
        "heel_stack_mm": 36,
        "forefoot_stack_mm": 28,
        "drop_mm": 8,
        "use_case": "tempo",
        "terrain": "road",
    },
    {
        "brand": "Saucony",
        "model": "Endorphin Pro 4",
        "weight_g": 212,
        "heel_stack_mm": 39.5,
        "forefoot_stack_mm": 31.5,
        "drop_mm": 8,
        "use_case": "racing",
        "terrain": "road",
    },
    {
        "brand": "adidas",
        "model": "Adizero Boston 13",
        "weight_g": 253,
        "heel_stack_mm": 36,
        "forefoot_stack_mm": 30,
        "drop_mm": 6,
        "use_case": "tempo",
        "terrain": "road",
    },
    {
        "brand": "Nike",
        "model": "Pegasus 41",
        "weight_g": 297,
        "heel_stack_mm": 37,
        "forefoot_stack_mm": 27,
        "drop_mm": 10,
        "use_case": "daily",
        "terrain": "road",
    },
]


def seed_database() -> None:
    """
    Populate database with shoes & brands.
    """
    with SessionLocal() as session:
        # Don't seed if the database already contains data.
        if session.scalar(select(Shoe.id).limit(1)) is not None:
            return

        brands = {
            name: Brand(name=name)
            for name in BRANDS
        }

        session.add_all(brands.values())
        session.flush()

        shoes = [
            Shoe(
                brand=brands[data["brand"]],
                model=data["model"],
                weight_g=data["weight_g"],
                heel_stack_mm=data["heel_stack_mm"],
                forefoot_stack_mm=data["forefoot_stack_mm"],
                drop_mm=data["drop_mm"],
                use_case=data["use_case"],
                terrain=data["terrain"],
            )
            for data in SHOES
        ]

        session.add_all(shoes)
        session.commit()