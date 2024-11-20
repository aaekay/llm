import requests
import json
import argparse
# from prompts_main import *
# Define the URL
url = "http://127.0.0.1:8000/generate/"

parser = argparse.ArgumentParser()

parser.add_argument("-f", type=str)

args = parser.parse_args()


# Define the data payload
data = {
    "impression": [
        {"role": "system", "content": "You are an AI assistant whose role is to listen to the user"},
        {"role": "user", "content": "Write a poem in 50 words about sun" },
    ]}

# Send the POST request
response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))

# Print the response
print(response.status_code)
print(response.json())

# let's test 10 requests sequentially
i = 0
while i < 10:
    response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))

    # Print the response
    print(response.status_code)
    print(response.json())
    i +=1

