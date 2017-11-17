import os

import pandas as pd
import requests

CSV_URL_BASE = "https://github.com/ombegov/policy-v2/raw/master/assets/"
CSV_URLS = (
    "Phase1_CombinedQA_AllPhase1_Nov21.csv",
    "AllPhasesCombinedTaggingTemp_Feb16.csv",
    "AllPhasesCombinedTaggingTemp_March28_for18f.csv",
)
CSV_URL = "{0}{1}".format(CSV_URL_BASE, CSV_URLS[-1])

def fetch(filename):
    # Most of this is adapted from:
    #
    # https://github.com/18F/omb-eregs/blob/master/api/reqs/management/commands/fetch_csv.py

    if not os.path.isfile(filename):
        print(f"Downloading {CSV_URL}...")
        response = requests.get(CSV_URL).content
        response_str = response.decode('cp1252')
        with open(filename, 'wb') as data_csv:
            data_csv.write(response_str.encode('utf8'))


def fetch_and_read(filename='data.csv'):
    fetch(filename)
    df = pd.read_csv(filename, converters=converters_for_labels())
    irrelevant_cols = [
        col for col in df.columns
        if not (col == 'reqText' or col in LABELS)
    ]
    for col in irrelevant_cols:
        del df[col]
    return df


def xbool(val):
    val = val.lower().strip()
    if val in ['x', 'z']:
        return True
    elif val in ['', '0']:
        return False
    raise ValueError(val)


LABELS = [
    'Human Capital',
    'Cloud',
    'Data Centers',
    'Cybersecurity',
    'Privacy',
    'Shared Services',
    'IT Project Management',
    'Software',
    'Digital Services',
    'Mobile',
    'Hardware/Government Furnished Equipment (GFE)',
    'IT Transparency (Open Data, FOIA, Public Records, etc.)',
    'Agency Statistics',
    'Customer Services',
    'Governance',
    'Financial Systems',
    'Budget',
    #'Governance - Org Structure',
    'Governance - Implementation',
    'Data Management/Standards',
    'Definitions',
    'Reporting',
    #'Other',
]


def converters_for_labels():
    converters = {}
    for label in LABELS:
        converters[label] = xbool
    return converters
