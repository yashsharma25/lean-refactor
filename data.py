import requests
import json

# Replace these variables with your own data
GITHUB_TOKEN = 'YOUR_GITHUB_TOKEN'
REPO_OWNER = 'owner'
REPO_NAME = 'repo'

# Construct the search query
query = 'refactor+golf+repo:{}/{}'.format(REPO_OWNER, REPO_NAME)

# Set up the headers with our token and the special header for using the search API
headers = {
    'Authorization': 'token {}'.format(GITHUB_TOKEN),
    'Accept': 'application/vnd.github.cloak-preview'
}

# The URL for the search commits API
url = 'https://api.github.com/search/commits?q={}'.format(query)

response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    commits = response.json()['items']
    
    for commit in commits:
        # Extract and print relevant information for each commit
        print("Commit message: {}".format(commit['commit']['message']))
        print("Author: {}".format(commit['commit']['author']['name']))
        print("Date: {}".format(commit['commit']['author']['date']))
        print("URL: {}".format(commit['html_url']))
        print("---")
else:
    print("Failed to fetch commits. Status code: {}".format(response.status_code))
