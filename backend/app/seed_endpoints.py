import json
from sqlalchemy.orm import Session
from .models import Endpoint
from .database import SessionLocal, engine, Base


# Define the endpoints to monitor
ENDPOINTS_CONFIG = [
    {
        "name": "Sandshrew Mainnet API",
        "url": "https://mainnet.sandshrew.io/v2",
        "method": "POST",
        "headers": json.dumps({"x-oyl-api-key": "d6aebfed1769128379aca7d215f0b689", "Content-Type": "application/json"}),
        "body": json.dumps({"method": "metashrew_height", "params": [], "id": 0, "jsonrpc": "2.0"}),
        "expected_status": 200,
    },
    {
        "name": "Metashrew API",
        "url": "https://metashrew.s.oyl.gg",
        "method": "POST",
        "headers": json.dumps({"Content-Type": "application/json"}),
        "body": json.dumps({"method": "metashrew_height", "params": [], "id": 0, "jsonrpc": "2.0"}),
        "expected_status": 200,
    },
    {
        "name": "Alkanes API",
        "url": "https://alkanes.oyl.gg",
        "method": "POST",
        "headers": json.dumps({"Content-Type": "application/json"}),
        "body": json.dumps({"method": "metashrew_height", "params": [], "id": 0, "jsonrpc": "2.0"}),
        "expected_status": 200,
    },
    {
        "name": "OYL App",
        "url": "https://app.oyl.io",
        "method": "GET",
        "headers": None,
        "body": None,
        "expected_status": 200,
    },
]


def seed_endpoints():
    """Seed the database with endpoints to monitor."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        for config in ENDPOINTS_CONFIG:
            # Check if endpoint already exists
            existing = db.query(Endpoint).filter(Endpoint.name == config["name"]).first()
            if not existing:
                endpoint = Endpoint(**config)
                db.add(endpoint)
                print(f"Added endpoint: {config['name']}")
            else:
                print(f"Endpoint already exists: {config['name']}")
        
        db.commit()
        print("Endpoints seeded successfully!")
    except Exception as e:
        print(f"Error seeding endpoints: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_endpoints()
