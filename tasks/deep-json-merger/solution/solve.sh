#!/bin/bash

# Overwrite the python script with a deep merge recursive function

RUN_CONTENT='import json

import sys

def deep_merge(d1, d2):

    for k, v in d2.items():

        if k in d1 and isinstance(d1[k], dict) and isinstance(v, dict):

            deep_merge(d1[k], v)

        else:

            d1[k] = v

    return d1

try:

    with open("/app/defaults.json", "r") as f:

        defaults = json.load(f)

    with open("/app/user_settings.json", "r") as f:

        user = json.load(f)

        

    result = deep_merge(defaults, user)

    with open("/tmp/merged_config.json", "w") as out:

        json.dump(result, out)

except Exception as e:

    print(f"Failed to merge configs: {e}", file=sys.stderr)

    sys.exit(1)'

echo -e "$RUN_CONTENT" > /app/merge_configs.py

# Run the script

python3 /app/merge_configs.py

