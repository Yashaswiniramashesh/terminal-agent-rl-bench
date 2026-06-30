import json

import sys


def deep_merge(d1, d2):

  # Bug: basic update overrides nested dicts instead of deep merging

  d1.update(d2)

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

  sys.exit(1)
