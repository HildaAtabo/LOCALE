import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import AsyncMock, patch, MagicMock
from models import Nigeria, Regions, States


client = TestClient(app)

#Mocking the db session

@pytest.fixture
def nigeria_db_session():
    with patch('main.SessionLocal') as mock:
        mock.return_value = MagicMock()
        yield mock

#Test for POST /region
def test_create_region(nigeria_db_session):
    test_region = {
        "name": "Test name",
        "state": "Test state"
    }
    response = client.post("/region", json=test_region) 
    assert response.status_code == 201
    assert response.json() ["name"] == "Test name"

#Test for POST /state
def test_create_state(nigeria_db_session):
    test_state = {
        "name": "Test name",
        "lga": "Test lga"
    }
    response = client.post("/state", json=test_state) 
    assert response.status_code == 201
    assert response.json() ["name"] == "Test name"


#Test Get all regions, states and lgas
def test_read_all(nigeria_db_session: MagicMock | AsyncMock):
    nigeria_db_session.return_value.query.return_value.all.return_value = [
        Nigeria(id=1, region="Test Nigeria", state="Test Nigeria"),
        Nigeria(id=2, region="Test Nigeria 2", state="Test Nigeria 2")
    ]
    response = client.get("/")
    assert response.status_code == 200
    assert len(response.json()) == 2

    

#Test Get one region by ID 
def test_read_one(nigeria_db_session: MagicMock | AsyncMock):
    nigeria_db_session.return_value.query.return_value.filter.return_value.first.return_value = Regions(id=1, state="Test Region")
    response =  client.get("/region/1")
    assert response.status_code == 200
    assert response.json()["state"] == "Test Region"

#Test Get one state by ID 
def test_read_one(nigeria_db_session: MagicMock | AsyncMock):
    nigeria_db_session.return_value.query.return_value.filter.return_value.first.return_value = States(id=1, lga="Test State")
    response =  client.get("/state/1")
    assert response.status_code == 200
    assert response.json()["lga"] == "Test State"

#Test for updating a region
def test_update_region(nigeria_db_session: MagicMock | AsyncMock):
    updated_region = {
        "state": "Test Region"
    }

#Test for updating a state
def test_update_state(nigeria_db_session: MagicMock | AsyncMock):
    updated_state = {
        "lga": "Test Region"
    }

#Test for deleting a region
def test_delete_region(nigeria_db_session: MagicMock | AsyncMock):
    response = client.delete("/region/1")
    assert response.status_code == 204

#Test for deleting a state
def test_delete_state(nigeria_db_session: MagicMock | AsyncMock):
    response = client.delete("/state/1")
    assert response.status_code == 204


