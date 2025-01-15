import json

import requests


def check_grid_status():
    url = "http://127.0.0.1:4444/status"  # Adjust the URL if needed
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(json.dumps(data, indent=4))  # Print the full Grid status for debugging
    except requests.RequestException as e:
        print(f"Error querying Grid status: {e}")


check_grid_status()
