from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

# Root test -> Sanity check
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Marine Park API!"}

# Check read item path
def test_read_item():
    response = client.get('/marine_parks/1')
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

# Check default read items path
def test_read_items():
    response = client.get('/marine_parks')
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 10

# Check kind query
def test_read_items_kind(kind: str = 'Special Purpose Zone'):
    response = client.get(f'/marine_parks?kind={kind}&limit=1')
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert kind in response.json()[0].get('ZONENAME')
    assert len(response.json()) == 1

# Check location query
def test_read_items_location(location: str = 'lord howe'):
    response = client.get(f'/marine_parks?location={location}&limit=1')
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert location.lower() in response.json()[0].get('RESNAME').lower()
    assert len(response.json()) == 1