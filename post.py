# Make a POST request to the JobTread API
# Command line arguments:
# - file name of the query
# - save the response in /responses (optional)
# Note: Uses .env file for configuration variables
# Prints a pretty JSON response or the error message
import requests
import os
import json
import argparse

def make_post_request(url, data):
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=4))
    else:
        print(response.text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='file name of the query')
    parser.add_argument('--save', action='store_true', help='save the response in /responses')
    args = parser.parse_args()

    with open(args.file, 'r') as f:
        data = f.read()

    url = os.getenv('JOBTREAD_URL')
    response = make_post_request(url, data)

    # Save the response in /responses
    if args.save:
        with open(f'responses/{args.file}.json', 'w') as f:
            f.write(response.text)  


if __name__ == '__main__':
    main()


# Example usage:
# python post.py query.pave --save
# python post.py query.pave