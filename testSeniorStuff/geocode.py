import asyncio
import aiohttp
import json

# Constants
TIMEOUT = 10  # seconds
REVERSE_GEOCODING_DELAY = 1


async def fetch_universities_in_bbox(session, south, west, north, east):
    query = f"""
    [out:json][timeout:180];
    (
      way["amenity"="university"]({south},{west},{north},{east});
      rel["amenity"="university"]({south},{west},{north},{east});
    );
    out center;
    >;
    out skel qt;
    """
    headers = {"Content-Type": "text/plain"}
    try:
        async with session.post("http://overpass-api.de/api/interpreter", data=query, headers=headers, timeout=TIMEOUT) as response:
            if response.content_type == 'application/json':
                data = await response.json()
                # Log fetched data
                print(
                    f"Data fetched for bbox {south},{west},{north},{east}: {data}")
                return data
            else:
                content = await response.text()
                print(
                    f"Non-JSON response for bbox {south},{west},{north},{east}: {content}")
                return None
    except Exception as e:
        print(f"Error in bbox {south},{west},{north},{east}: {e}")
        return None


async def reverse_geocode(session, latitude, longitude, university_name):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}"
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                country = data.get('address', {}).get('country', 'Unknown')
                # Detailed logging with university name
                print(
                    f"Reverse geocoding response for {university_name} ({latitude}, {longitude}): {country}")
                return country
            else:
                print(
                    f"Reverse geocoding failed for {university_name} ({latitude}, {longitude}): {response.status}")
                return 'Unknown'
    except Exception as e:
        print(
            f"Error in reverse geocoding for {university_name} ({latitude}, {longitude}): {e}")
        return 'Unknown'


async def main():
    universities = []
    async with aiohttp.ClientSession() as session:
        # Single bounding box covering a part of the eastern United States
        south, west, north, east = 40.0, -80.0, 45.0, -70.0
        print(
            f"Processing bounding box: South={south}, West={west}, North={north}, East={east}")
        response = await fetch_universities_in_bbox(session, south, west, north, east)
        if response and "elements" in response:
            for element in response["elements"]:
                if element["type"] == "way" or element["type"] == "relation":
                    if "tags" in element and "name" in element["tags"]:
                        latitude = element["center"]["lat"]
                        longitude = element["center"]["lon"]
                        university_name = element["tags"]["name"]
                        # Delay to avoid rate limit
                        # await asyncio.sleep(REVERSE_GEOCODING_DELAY)
                        country = await reverse_geocode(session, latitude, longitude, university_name)
                        universities.append({
                            "name": element["tags"]["name"],
                            "latitude": latitude,
                            "longitude": longitude,
                            "country": country
                        })
        else:
            print("No data or error for the specified bounding box.")

    json_output = json.dumps(universities, indent=4)
    with open('universities_single_bbox.json', 'w') as file:
        file.write(json_output)

    print("Finished processing a single bounding box.")

asyncio.run(main())