# Task: Implement Nested Dictionary Deep Merge

The Python script located at `/app/merge_configs.py` is intended to merge user-specified options in `/app/user_settings.json` with the base configuration template at `/app/defaults.json`, outputting the result to `/tmp/merged_config.json`.

Currently, the script is broken because it performs a shallow update:

`d1.update(d2)`

This shallow update completely overwrites nested configuration dictionaries (specifically the `features` dictionary), wiping out keys that weren't redefined by the user (like `beta_testing`).

Your objective:

1. Modify `/app/merge_configs.py` to perform a **deep merge** recursively if both dictionary keys point to nested dictionaries.

2. Run the script so that the combined, preserved configuration dictionary is written to `/tmp/merged_config.json`.

Constraints:

* Do not modify the output location of `/tmp/merged_config.json`.

* Only modify the `deep_merge` helper function inside `/app/merge_configs.py`.
