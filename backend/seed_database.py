"""
Database seeding script
Imports data from JSON files to Supabase
"""

import asyncio
import asyncpg
import json
import os
from pathlib import Path

DATABASE_URL = os.getenv("DATABASE_URL")

async def seed_database():
    """Seed database with initial data"""
    
    # Load JSON data
    data_dir = Path(__file__).parent.parent / "data"
    
    with open(data_dir / "places.json") as f:
        places_data = json.load(f)
    
    with open(data_dir / "questions.json") as f:
        questions_data = json.load(f)
    
    # Connect to database
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        # Insert places
        print("Inserting places...")
        for place in places_data:
            await conn.execute(
                """INSERT INTO places (name, category, description, image_url, characteristics)
                   VALUES ($1, $2, $3, $4, $5)
                   ON CONFLICT DO NOTHING""",
                place["name"],
                place["category"],
                place.get("description"),
                place.get("image_url"),
                json.dumps(place["characteristics"])
            )
        print(f"✅ Inserted {len(places_data)} places")
        
        # Insert questions
        print("Inserting questions...")
        for question in questions_data:
            await conn.execute(
                """INSERT INTO questions (text, characteristic, expected_value, category)
                   VALUES ($1, $2, $3, $4)
                   ON CONFLICT DO NOTHING""",
                question["text"],
                question["characteristic"],
                json.dumps(question["expected_value"]),
                question["category"]
            )
        print(f"✅ Inserted {len(questions_data)} questions")
        
        print("✅ Database seeded successfully!")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(seed_database())