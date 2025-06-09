import requests
import psycopg2
from psycopg2.extras import execute_values

DB_CONFIG = {
    "dbname": "spad02",
    "user": "postgres",
    "password": "123qwe",
    "host": "localhost",
    "port": 5432
}

API_URL = "https://api.rescuegroups.org/v5/public/animals/"

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
            distance TEXT,
            donationUrl TEXT,
            email TEXT,
            facebookUrl TEXT,
            fax TEXT,
            isCommonapplicationAccepted BOOLEAN,
            lat FLOAT,
            lon FLOAT,
            meetPets TEXT,
            name TEXT,
            phone TEXT,
            postcode TEXT,
            postcodePlus4 TEXT,
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

        CREATE TABLE IF NOT EXISTS Animals (
            id INTEGER PRIMARY KEY,
            activityLevel TEXT,
            adoptedDate TEXT,
            adoptionFeeString TEXT,
            adultSexesOK TEXT,
            ageGroup TEXT,
            ageString TEXT,
            availableDate TEXT,
            birthDate TEXT,
            breedPrimaryId INTEGER REFERENCES Breeds(id),
            breedSecondaryId INTEGER REFERENCES Breeds(id),
            breedString TEXT,
            coatLength TEXT,
            colorDetails TEXT,
            descriptionHtml TEXT,
            descriptionText TEXT,
            distinguishingMarks TEXT,
            earType TEXT,
            energyLevel TEXT,
            exerciseNeeds TEXT,
            eyeColor TEXT,
            fenceNeeds TEXT,
            foundDate TEXT,
            foundPostalcode TEXT,
            groomingNeeds TEXT,
            housetrainedReasonNot TEXT,
            indoorOutdoor TEXT,
            isAdoptionPending BOOLEAN,
            isAltered BOOLEAN,
            isBirthDateExact BOOLEAN,
            isBonded BOOLEAN,
            isCatOK BOOLEAN,
            isCourtesyListing BOOLEAN,
            isCurrentVaccinations BOOLEAN,
            isDeclawed BOOLEAN,
            isDogOK BOOLEAN,
            isFarmAnimalsOK BOOLEAN,
            isFound BOOLEAN,
            isHouseTrained BOOLEAN,
            isKidOK BOOLEAN,
            isMicrochipped BOOLEAN,
            isNeedingFoster BOOLEAN,
            isSeniorOK BOOLEAN,
            isSpecialNeeds BOOLEAN,
            isSpecialNeedsReason TEXT,
            isTestRequired BOOLEAN,
            killDate TEXT,
            killReason TEXT,
            name TEXT,
            newPeopleReaction TEXT,
            obedienceTraining TEXT,
            ownerExperience TEXT,
            pictureCount INTEGER,
            pictureThumbnailUrl TEXT,
            priority INTEGER,
            qualities TEXT,
            rescued TEXT,
            searchString TEXT,
            sex TEXT,
            sheddingLevel TEXT,
            sizeCurrent TEXT,
            sizeGroup TEXT,
            sizePotential TEXT,
            sizeOld TEXT,
            slug TEXT,
            specialNeedsDetails TEXT,
            sponsors TEXT,
            sponsorshipDetails TEXT,
            sponsorshipMinimum TEXT,
            summary TEXT,
            tailType TEXT,
            tracerImageUrl TEXT,
            updatedDate TEXT,
            url TEXT,
            videoCount INTEGER,
            videoUrlCount INTEGER,
            vocalLevel TEXT,
            organizationId INTEGER REFERENCES Organizations(id),
            speciesId INTEGER REFERENCES Species(id),
            patternId INTEGER REFERENCES Patterns(id),
            statusId INTEGER REFERENCES Statuses(id),
            locationId INTEGER REFERENCES Locations(id)
        );

        CREATE TABLE IF NOT EXISTS AnimalsPictures (
            id INTEGER PRIMARY KEY,
            animalId INTEGER REFERENCES Animals(id),
            created TEXT,
            large TEXT,
            "order" INTEGER,
            original TEXT,
            small TEXT,
            updated TEXT
        );

        CREATE TABLE IF NOT EXISTS Contacts (
            id INTEGER PRIMARY KEY,
            email TEXT,
            firstname TEXT,
            fullname TEXT,
            lastname TEXT,
            name TEXT,
            phoneCell TEXT,
            phoneHome TEXT,
            salutation TEXT,
            animalId INTEGER REFERENCES Animals(id)
        );

        CREATE TABLE IF NOT EXISTS Colors (
            id INTEGER PRIMARY KEY,
            name TEXT
        );
        """)
        conn.commit()

def extract_data():
    response = requests.get(API_URL, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def insert_data(conn, table, data, columns):
    reserved_words = {"order"}
    columns_escaped = [
        f'"{col}"' if col.lower() in reserved_words else col
        for col in columns
    ]

    if not data:
        return
    with conn.cursor() as cur:
        query = f"""
        INSERT INTO {table} ({', '.join(columns_escaped)})
        VALUES %s
        ON CONFLICT (id) DO NOTHING
        """
        execute_values(cur, query, data)

def transform_and_load(json_data, conn):
    animals_data = []
    pictures_data = []
    orgs = {}
    breeds = {}
    species = {}
    statuses = {}
    locations = {}

    for animal in json_data["data"]:
        a = animal["attributes"]
        rel = animal["relationships"]

        animals_data.append([
            int(animal["id"]),
            a.get("activityLevel"),
            a.get("adoptedDate"),
            a.get("adoptionFeeString"),
            None,  # adultSexesOK
            a.get("ageGroup"),
            a.get("ageString"),
            a.get("availableDate"),
            a.get("birthDate"),
            rel.get("breeds", {}).get("data", [{}])[0].get("id"),
            rel.get("breeds", {}).get("data", [{}])[1].get("id") if len(rel.get("breeds", {}).get("data", [])) > 1 else None,
            a.get("breedString"),
            a.get("coatLength"),
            a.get("colorDetails"),
            a.get("descriptionHtml"),
            a.get("descriptionText"),
            a.get("distinguishingMarks"),
            a.get("earType"),
            a.get("energyLevel"),
            a.get("exerciseNeeds"),
            a.get("eyeColor"),
            a.get("fenceNeeds"),
            a.get("foundDate"),
            a.get("foundPostalcode"),
            a.get("groomingNeeds"),
            a.get("housetrainedReasonNot"),
            a.get("indoorOutdoor"),
            a.get("isAdoptionPending"),
            a.get("isAltered"),
            a.get("isBirthDateExact"),
            a.get("isBonded"),
            a.get("isCatOK"),
            a.get("isCourtesyListing"),
            a.get("isCurrentVaccinations"),
            a.get("isDeclawed"),
            a.get("isDogOK"),
            a.get("isFarmAnimalsOK"),
            a.get("isFound"),
            a.get("isHouseTrained"),
            a.get("isKidOK"),
            a.get("isMicrochipped"),
            a.get("isNeedingFoster"),
            a.get("isSeniorOK"),
            a.get("isSpecialNeeds"),
            a.get("isSpecialNeedsReason"),
            a.get("isTestRequired"),
            a.get("killDate"),
            a.get("killReason"),
            a.get("name"),
            a.get("newPeopleReaction"),
            a.get("obedienceTraining"),
            a.get("ownerExperience"),
            a.get("pictureCount"),
            a.get("pictureThumbnailUrl"),
            a.get("priority"),
            a.get("qualities"),
            a.get("rescued"),
            a.get("searchString"),
            a.get("sex"),
            a.get("sheddingLevel"),
            a.get("sizeCurrent"),
            a.get("sizeGroup"),
            a.get("sizePotential"),
            a.get("sizeOld"),
            a.get("slug"),
            a.get("specialNeedsDetails"),
            a.get("sponsors"),
            a.get("sponsorshipDetails"),
            a.get("sponsorshipMinimum"),
            a.get("summary"),
            a.get("tailType"),
            a.get("trackerimageUrl"),
            a.get("updatedDate"),
            a.get("url"),
            a.get("videoCount"),
            a.get("videoUrlCount"),
            a.get("vocalLevel"),
            rel.get("orgs", {}).get("data", [{}])[0].get("id"),
            rel.get("species", {}).get("data", [{}])[0].get("id"),
            None,
            rel.get("statuses", {}).get("data", [{}])[0].get("id"),
            rel.get("locations", {}).get("data", [{}])[0].get("id")
        ])

    for included in json_data.get("included", []):
        attrs = included.get("attributes", {})
        inc_id = int(included["id"])

        match included["type"]:
            case "orgs":
                orgs[inc_id] = [
                    inc_id,
                    None, None, None, attrs.get("city"), attrs.get("citystate"),
                    attrs.get("coordinates"), attrs.get("country"), None,
                    None, attrs.get("email"), attrs.get("facebookUrl"), None,
                    None, attrs.get("lat"), attrs.get("lon"), None,
                    attrs.get("name"), attrs.get("phone"), attrs.get("postalcode"),
                    None, None, None, None,
                    attrs.get("state"), attrs.get("street"), attrs.get("type"), attrs.get("url")
                ]
            case "species":
                species[inc_id] = [
                    inc_id,
                    attrs.get("plural"),
                    attrs.get("singular"),
                    attrs.get("youngPlural"),
                    attrs.get("youngSingular")
                ]
            case "statuses":
                statuses[inc_id] = [inc_id, attrs.get("name"), attrs.get("description")]
            case "breeds":
                breeds[inc_id] = [inc_id, attrs.get("name")]
            case "locations":
                locations[inc_id] = [
                    inc_id, attrs.get("city"), attrs.get("citystate"), attrs.get("coordinates"),
                    attrs.get("country"), attrs.get("lat"), attrs.get("lon"), None, attrs.get("phone"),
                    None, attrs.get("postalcode"), None, attrs.get("state"),
                    attrs.get("street"), None
                ]
            case "pictures":
                pictures_data.append([
                    inc_id,
                    int(json_data["data"][0]["id"]),
                    None,
                    attrs.get("large", {}).get("url"),
                    attrs.get("order"),
                    attrs.get("original", {}).get("url"),
                    attrs.get("small", {}).get("url"),
                    attrs.get("updated")
                ])

    insert_data(conn, "Organizations", list(orgs.values()), [col for col in [
        "id", "about", "adoptionProcess", "adoptionUrl", "city", "citystate", "coordinates",
        "country", "distance", "donationUrl", "email", "facebookUrl", "fax", "isCommonapplicationAccepted",
        "lat", "lon", "meetPets", "name", "phone", "postcode", "postcodePlus4", "serveAreas",
        "services", "sponsorshipUrl", "state", "street", "type", "url"
    ]])
  
    insert_data(conn, "Species", list(species.values()), ["id", "plural", "singular", "youngPlural", "youngSingular"])
    insert_data(conn, "Statuses", list(statuses.values()), ["id", "name", "description"])
    insert_data(conn, "Breeds", list(breeds.values()), ["id", "name"])
    insert_data(conn, "Locations", list(locations.values()), [
        "id", "city", "citystate", "coordinates", "country", "lat", "lon",
        "name", "phone", "phoneExt", "postalCode", "postalCodePlus4",
        "state", "street", "url"
    ])
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM Animals LIMIT 0")
        columns = [desc.name for desc in cur.description]

    insert_data(conn, "Animals", animals_data, columns)

    
    
    insert_data(conn, "AnimalsPictures", pictures_data, [
        "id", "animalId", "created", "large", "order", "original", "small", "updated"
    ])
    
    
def main():
    data = extract_data()
    print(data)
    with psycopg2.connect(**DB_CONFIG) as conn:
        create_tables(conn) 
        transform_and_load(data, conn)
        conn.commit()

if __name__ == "__main__":
    main()
