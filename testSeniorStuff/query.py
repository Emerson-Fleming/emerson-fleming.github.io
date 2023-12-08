import asyncio
import aiohttp
import json

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
        async with session.post("http://overpass-api.de/api/interpreter", data=query, headers=headers) as response:
            if response.content_type == 'application/json':
                return await response.json()
            else:
                content = await response.text()
                print(
                    f"Non-JSON response for bbox {south},{west},{north},{east}: {content}")
                return None
    except Exception as e:
        print(f"Error in bbox {south},{west},{north},{east}: {e}")
        return None

async def main():
    bounding_boxes = [(lat, lon, lat + 60, lon + 60)
                      for lat in range(-90, 90, 60) for lon in range(-180, 180, 60)]
    universities = []
    async with aiohttp.ClientSession() as session:
        for i, bbox in enumerate(bounding_boxes):
            print(
                f"Processing bounding box {i+1}/{len(bounding_boxes)}: {bbox}")
            response = await fetch_universities_in_bbox(session, *bbox)
            if response:
                for element in response["elements"]:
                    if element["type"] == "way" or element["type"] == "relation":
                        if "tags" in element and "name" in element["tags"]:
                            universities.append({
                                "name": element["tags"]["name"],
                                "latitude": element["center"]["lat"],
                                "longitude": element["center"]["lon"]
                            })

    json_output = json.dumps(universities, indent=4)
    with open('universities_worldwide_async.json', 'w') as file:
        file.write(json_output)
    print("Finished processing universities.")

asyncio.run(main())