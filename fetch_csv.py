import os

import requests

# Most of this is adapted from:
#
# https://github.com/18F/omb-eregs/blob/master/api/reqs/management/commands/fetch_csv.py

CSV_URL_BASE = "https://github.com/ombegov/policy-v2/raw/master/assets/"
CSV_URLS = (
    "Phase1_CombinedQA_AllPhase1_Nov21.csv",
    "AllPhasesCombinedTaggingTemp_Feb16.csv",
    "AllPhasesCombinedTaggingTemp_March28_for18f.csv",
)
CSV_URL = "{0}{1}".format(CSV_URL_BASE, CSV_URLS[-1])

def fetch(filename):
    if not os.path.isfile(filename):
        print(f"Downloading {CSV_URL}...")
        response = requests.get(CSV_URL).content
        response_str = response.decode('cp1252')
        with open(filename, 'wb') as data_csv:
            data_csv.write(response_str.encode('utf8'))
    else:
        print(f"{filename} already exists, skipping.")
