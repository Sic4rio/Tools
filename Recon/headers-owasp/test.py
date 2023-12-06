import requests
import json

# Load the JSON data
with open('headers_add.json') as json_file:
    headers_data = json.load(json_file)

def colorize(text, color):
    colors = {
        'reset': '\033[0m',
        'green': '\033[32m',
        'red': '\033[31m'
    }
    return f"{colors[color]}{text}{colors['reset']}"

def check_headers(url):
    try:
        # Make a request to the URL
        response = requests.get(url)
        headers = response.headers

        # Count missing headers
        missing_headers = 0

        # List of missing headers
        missing_headers_list = []

        # Check each header
        for header in headers_data['headers']:
            header_name = header['name']
            header_value = header['value']

            if header_name in headers and headers[header_name] == header_value:
                pass
            else:
                missing_headers += 1
                missing_headers_list.append(f"{colorize('✘', 'red')} {header_name}: {header_value}")

        # Print missing headers
        if missing_headers > 0:
            print(f"\n{colorize(str(missing_headers) + ' missing headers:', 'red')}")
            for missing_header in missing_headers_list:
                print(missing_header)

        # Print present headers
        print(f"\n{colorize('Present headers:', 'green')}")
        for header_name, header_value in headers.items():
            print(f"{colorize('✔', 'green')} {header_name}: {header_value}")

    except requests.RequestException as e:
        print(f"\nError making request to {url}: {e}")

if __name__ == "__main__":
    # Take user input for the domain
    domain = input("Enter the domain (e.g., https://example.com): ")
    
    # Check headers for the provided domain
    check_headers(domain)

