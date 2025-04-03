from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from pandas import read_csv
import uvicorn
import os

# 1. Initialize FastAPI app
app = FastAPI(
    title="Marine Park API",
    description="An API to demonstrate querying marine park locations",
    version="0.0.1",
)

# 2. Define your data model using Pydantic
# This ensures data validation and structures your responses.
class MarineParkLocation(BaseModel):
    OBJECTID: int
    NETNAME: str
    RESNAME: str
    ZONENAME: str
    ZONEIUCN: str
    POLYGONID: str
    NATLEGEND: str
    AREA_KM2: float
    SHAPEAREA: float
    SHAPELEN: float


# 3. Simulate a Data Source (Replace this with actual DB connection later)
# Using a list of dictionaries for simplicity.
marine_parks = read_csv('data/Australian_Marine_Parks.csv').to_dict(orient='records')

# 4. Root Endpoint (optional, good for health checks)
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Queryable Item API!"}

# 5. Endpoint to get multiple items with querying/filtering
#    - Uses Query Parameters: skip, limit, name_contains
#    - Uses `response_model` to structure the output based on the Pydantic model.
@app.get("/marine_parks/", response_model=List[MarineParkLocation])
async def read_items(
    skip: int = 0,                      # Default value 0 for pagination start
    limit: int = 10,                    # Default value 10 for pagination size
    location: Optional[str] = Query(None, description="Filter items by name containing this string (case-insensitive)"), # Optional query filter
    kind: Optional[str] = Query(None, description="Filter items by type containing this string (case-insensitive)"), # Optional query filter
):
    """
    Retrieve a list of items with optional filtering and pagination.
    """
    results = marine_parks

    # Apply filtering logic (simulating DB queries)
    if location:
        results = [item for item in results if location.lower() in item.get("RESNAME", "").lower()]

    if kind:
        results = [item for item in results if kind.lower() in item.get("ZONENAME", "").lower()]

    # Apply pagination
    paginated_results = results[skip : skip + limit]

    # Pydantic will automatically validate the output against List[Item]
    return paginated_results

# 6. Endpoint to get a specific item by its ID
#    - Uses a Path Parameter: item_id
#    - Includes error handling for items not found.
@app.get("/marine_parks/{OBJECTID}", response_model=MarineParkLocation)
async def read_item(OBJECTID: int):
    """
    Retrieve a single item by its unique ID.
    """
    # Find the item in our fake DB
    marine_park = next((marine_park for marine_park in marine_parks if marine_park["OBJECTID"] == OBJECTID), None)
    if marine_park is None:
        raise HTTPException(status_code=404, detail=f"marine park with ID {OBJECTID} not found")
    # Pydantic validates the output against the Item model
    return marine_park

def cli_run(host: str = "127.0.0.1", port: int = 8000, reload: bool = True):
    """Runs the FastAPI app using Uvicorn."""
    print(f"Starting Queryable Item API server on http://{host}:{port}")
    uvicorn.run(
        "main:app", # Path to the app instance
        host=host,
        port=port,
        reload=reload,
    )