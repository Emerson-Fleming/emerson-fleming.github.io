import requests
import json

# DID I DO PAGINATION CORRECTLY????
def fetch_universities(page=1, per_page=200):
    url = "https://api.openalex.org/institutions"
    params = {
        'per-page': per_page,
        'page': page,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()['results']
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return []


def write_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def main():
    all_universities = []
    for page in range(1, 11):
        print(f"Fetching page {page}...")
        universities = fetch_universities(page)
        all_universities.extend(universities)

    write_to_json(all_universities, 'openalex_universities.json')


if __name__ == '__main__':
    main()