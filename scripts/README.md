# Scripts

Utility scripts for the project. These are accessed through the `dev` CLI

## `dev upgrade`

Upgrade a dependency in all `pyproject.toml` files in the project. Is interactive - will display proposed 
change and ask for confirmation before making any changes.

Example:

```bash
python scripts/upgrade_deps.py conclib 0.0.1 0.0.2
```

NOTE: does not upgrade requirements.txt files, but could be changed to do that easily enough 
if desired.

## `dev sync`

Watches a directory and syncs it to a VM when the contents change. Edit code on your local machine,
test in on a GPU one. Hardcoded to ubuntu.

Has dependency on `rsync`.


## `dev gpu-work`

PyTorch matmuls to cause GPU to be used.
