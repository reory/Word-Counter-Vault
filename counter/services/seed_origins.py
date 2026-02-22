# This is to set up the DuckDB databse.
# idempotency (the ability to run a script multiple times without breaking things)
import duckdb
import os
import json
import django
from django.conf import settings

# This tells the script which settings file to use.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wordcounterapp.settings')
django.setup()

def seed_vault():

    # Define paths.
    db_path = os.path.join(settings.BASE_DIR, 'word_vault_analytics.duckdb')

    # Path to the JSON file with the words.
    json_path = os.path.join(settings.BASE_DIR, 'counter', 'services', 'word_data.json')

    # Load the JSON data.
    if not os.path.exists(json_path):
        print(f'Error: Could not find {json_path}')
        return
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # Connect to DuckDB.
    con = duckdb.connect(db_path)

    # Create the table.
    con.execute("""
        CREATE OR REPLACE TABLE origins (
            word VARCHAR, 
            root VARCHAR, 
            country VARCHAR, 
            lat DOUBLE, 
            lng DOUBLE, 
            fact TEXT
        )
    """)

    # Prepare the table for bulk insertion.
    all_rows = []
    for hub in data['hubs']:
        origin_name = hub['origin']
        country = hub['country']
        lat = hub['lat']
        lng = hub['lng']
        fact = hub['fact']

        for word in hub['words']:
            # Store everything in lowercase to make matching easier.
            all_rows.append((word.lower(), origin_name, country, lat, lng, fact))

    # Execute Bulk Insert 
    con.executemany('INSERT INTO origins VALUES (?, ?, ?, ?, ?, ?)', all_rows)

    # Verify the results
    count = con.execute('SELECT count(*) FROM origins').fetchone()[0] #type:ignore
    con.close()

    print(f'\nDone! Database now contains {count} words')

if __name__ == "__main__":
    seed_vault()