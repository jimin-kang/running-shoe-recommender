from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from shoe_recommender.database.models.brand import Brand
from shoe_recommender.database.models.shoe import Shoe
from shoe_recommender.schemas.preference import PreferenceRequest
from sqlalchemy.orm import sessionmaker, Session

from shoe_recommender.main import app


# Test suite
client = TestClient(app)

def test_get_shoe_not_found(db_session):
    """
    Test getting a non-existent shoe.
    """
    create_shoes(db_session)
    
    shoe_id = 999
    response = client.get(f"/api/shoes/{shoe_id}")
    
    response_data = response.json()
    assert response.status_code == 404
    assert "shoe not found" in response_data["detail"].lower()
    
    
def test_recommendation(db_session):
    """
    Verify user recommendations are correct.
    """
    
    # Check that user that prefers responsiveness gets the Saucony & Hoka returned as top recommendations
    # create_shoes(db_session)
    # user_preference = PreferenceRequest()
    # response = client.get(
    #     f"api/recommendation",
    #     json={
    #         # INSERT PREFERENCES HERE        
    #     }
    # )
    
    
    # assert response.status_code == 200
    # shoe_recs = response.recommendations
    # assert shoe_recs[0].shoe == "Hoka Mach 6" and shoe_recs[1].shoe == "Saucony Endorphin Speed 5"
  
    
def create_shoes(db_session):
    """
    Create mock shoe database.
    """
    saucony = Brand(name="Saucony")
    asics = Brand(name="ASICS")

    db_session.add_all([saucony, asics])

    speed_5 = Shoe(
        brand=saucony,
        model="Endorphin Speed 5",
        weight_g=237,
        heel_stack_mm=36,
        forefoot_stack_mm=28,
        drop_mm=8,
        use_case="tempo",
        terrain="road",
    )

    novablast = Shoe(
        brand=asics,
        model="Novablast 5",
        weight_g=255,
        heel_stack_mm=42,
        forefoot_stack_mm=34,
        drop_mm=8,
        use_case="daily",
        terrain="road",
    )

    db_session.add_all([speed_5, novablast])
    db_session.commit()