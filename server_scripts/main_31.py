import requests
import json
import argparse
from prompts_main import *
# Define the URL
url = "http://127.0.0.1:8000/generate/"

import argparse


# Define the data payload
data = {
    "impression": [
        {"role": "system", "content": "You are an AI assistant whose role is to listen to the user"},
        {"role": "user", "content": "Write a poem in 50 words about sun" },
    ],
    "token" : 250}

# Send the POST request
response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))

# Print the response
print(response.status_code)
print(response.json())

parser = argparse.ArgumentParser()
parser.add_argument("-prompt", type=str, default ="prompt_general")
parser.add_argument("-trial", type=int, default =1)
parser.add_argument("-sample", type=int, default=0)
parser.add_argument("-model", type=str)
parser.add_argument("-token", type=int, default=250)
parser.add_argument("-reports_c", type=str, default="report")
parser.add_argument("-accession_c", type=str, default="patient_id")
parser.add_argument("-file", type=str, default="sample.csv"
                    )

args = parser.parse_args()

print(args)

def execute_function(function_name, impression, token):
    try:
        # Use globals() to get the function by its string name and execute it
        func = globals()[function_name]
        return func(impression, token)
    except KeyError:
        print(f"Function '{function_name}' is not defined.")
    except TypeError:
        print(f"'{function_name}' is not callable.")


import json
import pandas as pd

file = args.file
df = pd.read_csv(args.file)
filename = file.split("/")[-1]

print(df.columns)
df.dropna(inplace=True)
if args.sample:
    df = df[:args.sample]

impressions = df[args.reports_c].to_list()
accessions = df[args.accession_c].to_list()

print(len(impressions))
print(len(accessions))
import json

try:
    loaded_dict = {}
    with open(f'{args.model}_trial_{args.trial}_{args.token}_outputs_{args.prompt}_{filename}.txt', 'r') as file:
        for line in file:
            # Strip any extra whitespace and split on the colon and space
            val = line.strip()
            temp_dict = json.loads(val)
            for k,v in temp_dict.items():
                loaded_dict[k] = v
except:
    print("output json dont exist")
    loaded_dict = {}

from tqdm import tqdm
with open(f'{args.model}_trial_{args.trial}_{args.token}_outputs_{args.prompt}_{filename}.txt', 'a') as file:
    for i in tqdm(range(len(accessions))):
        if accessions[i] not in loaded_dict.keys():
            try:
                word_count = len(impressions[i].split())
                if 3*word_count < args.token:
                    output_token = args.token
                else:
                    output_token = 3*word_count 
                data = execute_function(args.prompt, impressions[i], output_token)
                # print(impressions[i])
                response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))
                # print(response.json()['generated_text'])
                # 'a' for append mode
                temp_dict = {accessions[i]: response.json()["generated_text"]}
                file.write(json.dumps(temp_dict) + "\n")
                print(i)
            except Exception as E:
                print(E)
                temp_dict = {accessions[i]: "Error in Inferencing"}
                file.write(json.dumps(temp_dict) + "\n")
        else:
            print(i)

