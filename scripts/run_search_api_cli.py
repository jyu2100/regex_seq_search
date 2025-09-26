import argparse
import json
import requests
import sys

def main():
    parser = argparse.ArgumentParser(description="Regex search via API (GET request)")
    parser.add_argument("pattern", type=str, help="Regex pattern")
    parser.add_argument("uid", type=str, help="UID")
    args = parser.parse_args()

    url = 'http://127.0.0.1:8000/api/sequences/'

    try:
        # Send GET request with query parameters
        response = requests.get(
            url,
            params={"pattern": args.pattern, "uid": args.uid}
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
        sys.exit(1)

    data = response.json()
    matches = json.loads(data)
    
    for sequence in matches:
        print(f'{sequence}')

        for start, end in matches[sequence]:
            print(f'  {start}-{end}')

        print('')

if __name__ == "__main__":
    main()
