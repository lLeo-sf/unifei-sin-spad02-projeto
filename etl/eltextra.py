import requests
import psycopg2
from psycopg2.extras import execute_values

DB_CONFIG = {
    "dbname": "rescue",
    "user": "postgres",
    "password": "admin",
    "host": "localhost",
    "port": 5432
}

API_URL = "https://api.rescuegroups.org/v5/"
HEADERS = {
    "Authorization": "MhmB89ht"
}

def create_additional_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Locations (
            id INTEGER PRIMARY KEY,
            city TEXT,
            citystate TEXT,
            coordinates TEXT,
            country TEXT,
            lat FLOAT,
            lon FLOAT,
            name TEXT,
            phone TEXT,
            phoneExt TEXT,
            postalCode TEXT,
            postalCodePlus4 TEXT,
            state TEXT,
            street TEXT,
            url TEXT
        );
        """)
        conn.commit()

def insert_data(conn, table, data, columns):
    if not data:
        print(f"No data to insert into {table}.")
        return
    with conn.cursor() as cur:
        query = f"""
        INSERT INTO {table} ({', '.join(columns)})
        VALUES %s
        ON CONFLICT DO NOTHING
        """
        print(f"Inserting {len(data)} records into {table}...")
        execute_values(cur, query, data)
    conn.commit()

def fetch_and_insert_locations(conn):
    page = 1
    limit = 250
    MAX_PAGES = 4000

    while page <= MAX_PAGES:
        print(f"Fetching animals (page={page})...")
        params = {"limit": limit, "page": page, "includes": "locations"}
        response = requests.get(f"{API_URL}public/animals/", headers=HEADERS, params=params)
        response.raise_for_status()
        json_data = response.json()

        locations = []
        included = json_data.get("included", [])
        for item in included:
            if item.get("type") == "locations":
                attrs = item.get("attributes", {})
                locations.append([
                    int(item["id"]),
                    attrs.get("city"), attrs.get("citystate"), attrs.get("coordinates"),
                    attrs.get("country"), attrs.get("lat"), attrs.get("lon"), None, attrs.get("phone"),
                    None, attrs.get("postalcode"), None, attrs.get("state"),
                    attrs.get("street"), None
                ])

        insert_data(conn, "Locations", locations, [
            "id", "city", "citystate", "coordinates", "country", "lat", "lon",
            "name", "phone", "phoneExt", "postalCode", "postalCodePlus4",
            "state", "street", "url"
        ])

        print(f"✔ Página {page} processada.")

        meta = json_data.get("meta", {})
        total_pages = min(meta.get("pages", 1), MAX_PAGES)
        if page >= total_pages:
            break
        page += 1

def main():
    with psycopg2.connect(**DB_CONFIG) as conn:
        create_additional_tables(conn)
        fetch_and_insert_locations(conn)

if __name__ == "__main__":
    main()
