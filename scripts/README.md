# Scripts

Utility scripts for the project

## `upgrade_deps.py`

Upgrade a dependency in all `pyproject.toml` files in the project. Is interactive - will display proposed 
change and ask for confirmation before making any changes.

Example:

```bash
python scripts/upgrade_deps.py conclib 0.0.1 0.0.2
```

NOTE: does not upgrade requirements.txt files, but could be changed to do that easily enough 
if desired.

## `sync_file_with_vm.py`

```
rsync
```

Watches a file and syncs it to a VM when it changes.