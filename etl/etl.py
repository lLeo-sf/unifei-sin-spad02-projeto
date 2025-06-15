import requests
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime

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

def create_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Organizations (
            id INTEGER PRIMARY KEY,
            about TEXT,
            adoptionProcess TEXT,
            adoptionUrl TEXT,
            city TEXT,
            citystate TEXT,
            coordinates TEXT,
            country TEXT,
            donationUrl TEXT,
            email TEXT,
            facebookUrl TEXT,
            isCommonapplicationAccepted BOOLEAN,
            lat FLOAT,
            lon FLOAT,
            name TEXT,
            phone TEXT,
            serveAreas TEXT,
            services TEXT,
            sponsorshipUrl TEXT,
            state TEXT,
            street TEXT,
            type TEXT,
            url TEXT
        );

        CREATE TABLE IF NOT EXISTS Species (
            id INTEGER PRIMARY KEY,
            plural TEXT,
            singular TEXT,
            youngPlural TEXT,
            youngSingular TEXT
        );

        CREATE TABLE IF NOT EXISTS Patterns (
            id INTEGER PRIMARY KEY,
            name TEXT
        );

        CREATE TABLE IF NOT EXISTS Breeds (
            id INTEGER PRIMARY KEY,
            name TEXT
        );

        CREATE TABLE IF NOT EXISTS Statuses (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT
        );

        CREATE TABLE IF NOT EXISTS Animals (
            id INTEGER PRIMARY KEY,
            name TEXT,
            speciesId INTEGER REFERENCES Species(id),
            breedPrimaryId INTEGER REFERENCES Breeds(id),
            breedSecondaryId INTEGER REFERENCES Breeds(id),
            patternId INTEGER REFERENCES Patterns(id),
            statusId INTEGER REFERENCES Statuses(id),
            organizationId INTEGER REFERENCES Organizations(id),
            activityLevel	TEXT,
            adoptedDate	DATE,
            ageGroup	TEXT,
            availableDate	DATE,
            breedPrimary	TEXT,
            breedSecondary	TEXT,
            coatLength	TEXT,
            colorDetails	TEXT,
            createdDate	DATE,
            energyLevel	TEXT,
            fenceNeeds	TEXT,
            foundDate	DATE,
            foundPostalcode	TEXT,
            indoorOutdoor	TEXT,
            isAdoptionPending	BOOLEAN,
            isBreedMixed	BOOLEAN,
            isCatsOk	BOOLEAN,
            isCurrentVaccinations	BOOLEAN,
            isDogsOk	BOOLEAN,
            isHousetrained	BOOLEAN,
            isKidsOk	BOOLEAN,
            isNeedingFoster	BOOLEAN,
            isSpecialNeeds	BOOLEAN,
            isSponsorable	BOOLEAN,
            isYardRequired	BOOLEAN,
            newPeopleReaction	TEXT,
            obedienceTraining	TEXT,
            priority	TEXT,
            rescueId	TEXT,
            sex	TEXT,
            sizeGroup	TEXT,
            specialNeedsDetails	TEXT,
            sponsorshipMinimum	TEXT,
            updatedDate	DATE
        );
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
        ON CONFLICT (id) DO NOTHING
        """
        print(f"Inserting {len(data)} records into {table}...")
        print(data)
        execute_values(cur, query, data)
    conn.commit()

def fetch_paginated_and_insert_animals(conn):
    page = 1
    limit = 250
    MAX_PAGES = 4898

    while page <= MAX_PAGES:
        params = {"limit": limit, "page": page, "include": "locations,species,breeds,statuses,patterns,orgs"}
        print(f"Fetching public/animals/ (page={page})...")
        response = requests.get(f"{API_URL}public/animals/", headers=HEADERS, params=params)
        response.raise_for_status()
        json = response.json()

        data = json.get("data", [])
        included = json.get("included", [])
        meta = json.get("meta", {})
        pages = meta.get("pages", 1)

        species = {}
        breeds = {}
        statuses = {}
        patterns = {}
        animals = []
        locations = {}
        orgs = {}

        for item in included:
            id_ = int(item["id"])
            attrs = item["attributes"]
            match item["type"]:
                case "species":
                    species[id_] = [id_, attrs.get("plural"), attrs.get("singular"), attrs.get("youngPlural"), attrs.get("youngSingular")]
                case "breeds":
                    breeds[id_] = [id_, attrs.get("name")]
                case "orgs":
                    orgs[id_] = [id_]
                
                case "statuses":
                    statuses[id_] = [id_, attrs.get("name"), attrs.get("description")]
                case "patterns":
                    patterns[id_] = [id_, attrs.get("name")]
                case "locations":
                    locations[id_] =  [id_, attrs.get("city"), attrs.get("citystate"), attrs.get("coordinates"),
                    attrs.get("country"), attrs.get("lat"), attrs.get("lon"), attrs.get("name"), attrs.get("phone"), attrs.get("phoneExt"), attrs.get("postalcode"), 
                    attrs.get("postalCodePlus4"), attrs.get("state"), attrs.get("street"), attrs.get("url")]
                    


        for a in data:
            r = a["relationships"]
            animals.append([
                int(a["id"]),
                a["attributes"].get("name"),
                r.get("species", {}).get("data", [{}])[0].get("id"),
                r.get("breeds", {}).get("data", [{}])[0].get("id"),
                r.get("breeds", {}).get("data", [{}])[1].get("id") if len(r.get("breeds", {}).get("data", [])) > 1 else None,
                r.get("patterns", {}).get("data", [{}])[0].get("id"),
                r.get("statuses", {}).get("data", [{}])[0].get("id"),
                r.get("orgs", {}).get("data", [{}])[0].get("id"),
                a["attributes"].get("activityLevel"),
                safe_parse_date(a["attributes"].get("adoptedDate")),
                a["attributes"].get("ageGroup"),
                safe_parse_date(a["attributes"].get("availableDate")),
                a["attributes"].get("breedPrimary"),
                a["attributes"].get("breedSecondary"),
                a["attributes"].get("coatLength"),
                a["attributes"].get("colorDetails"),
                safe_parse_date(a["attributes"].get("createdDate")),
                a["attributes"].get("energyLevel"),
                a["attributes"].get("fenceNeeds"),
                safe_parse_date(a["attributes"].get("foundDate")),
                a["attributes"].get("foundPostalcode"),
                a["attributes"].get("indoorOutdoor"),
                a["attributes"].get("isAdoptionPending"),
                a["attributes"].get("isBreedMixed"),
                a["attributes"].get("isCatsOk"),
                a["attributes"].get("isCurrentVaccinations"),
                a["attributes"].get("isDogsOk"),
                a["attributes"].get("isHousetrained"),
                a["attributes"].get("isKidsOk"),
                a["attributes"].get("isNeedingFoster"),
                a["attributes"].get("isSpecialNeeds"),
                a["attributes"].get("isSponsorable"),
                a["attributes"].get("isYardRequired"),
                a["attributes"].get("newPeopleReaction"),
                a["attributes"].get("obedienceTraining"),
                a["attributes"].get("priority"),
                a["attributes"].get("rescueId"),
                a["attributes"].get("sex"),
                a["attributes"].get("sizeGroup"),

                a["attributes"].get("specialNeedsDetails"),
                a["attributes"].get("sponsorshipMinimum"),
                safe_parse_date(a["attributes"].get("updatedDate"))

            ])

        animals = [a for a in animals if all([a[2], a[3], a[6]])]  


        insert_data(conn, "Species", list(species.values()), ["id", "plural", "singular", "youngPlural", "youngSingular"])
        insert_data(conn, "Breeds", list(breeds.values()), ["id", "name"])
        
        insert_data(conn, "Statuses", list(statuses.values()), ["id", "name", "description"])
        insert_data(conn, "Patterns", list(patterns.values()), ["id", "name"])
        insert_data(conn, "Animals", animals, [
            "id", "name", "speciesId", "breedPrimaryId", "breedSecondaryId",
            "patternId", "statusId","organizationId", "activityLevel", "adoptedDate", "ageGroup", "availableDate",
            "breedPrimary", "breedSecondary", "coatLength", "colorDetails", "createdDate",
            "energyLevel", "fenceNeeds", "foundDate", "foundPostalcode", "indoorOutdoor", "isAdoptionPending", 
            "isBreedMixed", "isCatsOk", "isCurrentVaccinations", "isDogsOk", "isHousetrained", "isKidsOk", 
            "isNeedingFoster", "isSpecialNeeds", "isSponsorable", "isYardRequired",  "newPeopleReaction", "obedienceTraining",
            "priority", "rescueId", "sex", "sizeGroup", "specialNeedsDetails", "sponsorshipMinimum", "updatedDate"	
        ])
        insert_data(conn, "Locations", list(locations.values()), ["id", "city", "citystate", "coordinates", "country", "lat", "lon",
        "name", "phone", "phoneExt", "postalCode", "postalCodePlus4", "state", "street", "url"
        ])

        print(f"✔ Página {page} processada e comitada com sucesso.")

        if page >= pages or page >= MAX_PAGES:
            break
        page += 1
def fetch_paginated_and_insert_orgs(conn):
    page = 1
    limit = 250
    MAX_PAGES = 4000

    while page <= MAX_PAGES:
        params = {"limit": limit, "page": page, }
        print(f"Fetching public/orgs/ (page={page})...")
        response = requests.get(f"{API_URL}public/orgs", headers=HEADERS, params=params)
        response.raise_for_status()
        json = response.json()

        data = json.get("data", [])
        meta = json.get("meta", {})
        pages = meta.get("pages", 1)
        
        columns = [
            "id", "about", "adoptionProcess", "adoptionUrl", "city", "citystate", "coordinates",
            "country", "donationUrl", "email", "facebookUrl", "isCommonapplicationAccepted",
            "lat", "lon", "name", "phone", "serveAreas",
            "services", "sponsorshipUrl", "state", "street", "type", "url"
        ]

        orgs = []
        for org in data:
            attrs = org.get("attributes", {})
            orgs.append(tuple([
                int(org["id"]),
                attrs.get("about"),
                attrs.get("adoptionProcess"),
                attrs.get("adoptionUrl"),
                attrs.get("city"),
                attrs.get("citystate"),
                attrs.get("coordinates"),
                attrs.get("country"),
                attrs.get("donationUrl"),
                attrs.get("email"),
                attrs.get("facebookUrl"),
                attrs.get("isCommonapplicationAccepted"),
                attrs.get("lat"),
                attrs.get("lon"),
                attrs.get("name"),
                attrs.get("phone"),
                attrs.get("serveAreas"),
                attrs.get("services"),
                attrs.get("sponsorshipUrl"),
                attrs.get("state"),
                attrs.get("street"),
                attrs.get("type"),
                attrs.get("url")
            ]))

        insert_data(conn, "Organizations", orgs, columns)
        
        print(f"✔ Página {page} processada e comitada com sucesso.")

        if page >= pages or page >= MAX_PAGES:
            break
        page += 1


def safe_parse_date(date_str):
    try:
        return datetime.strptime(date_str[:10], '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return None

    
def main():
    with psycopg2.connect(**DB_CONFIG) as conn:
        create_tables(conn)
        fetch_paginated_and_insert_animals(conn)
        fetch_paginated_and_insert_orgs(conn)

if __name__ == "__main__":
    main()
