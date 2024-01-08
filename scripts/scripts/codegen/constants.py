from pathlib import Path
from git import Repo

root = Path(Repo(".", search_parent_directories=True).working_tree_dir)

TEMPLATES = ["types", "datastore-client", "rest"]
CODEGENVARS_DIR = root / "scripts/codegen/codegenvars"
TYPES_TEMPLATE = (
    root / "controlplane/controlplane/datastore/types/vmmetrics/types.template"
)
TYPES_GENERATED_DIR = (
    root / "controlplane/controlplane/datastore/types/vmmetrics/generated"
)
DATASTORE_CLIENT_TEMPLATE = root / "controlplane/controlplane/datastore/client.template"
DATASTORE_CLIENT_IMPLEMENTATION = root / "controlplane/controlplane/datastore/client.py"
REST_API_TEMPLATE = root / "controlplane/controlplane/rest/rest.template"
REST_API_IMPLEMENTATION = root / "controlplane/controlplane/rest/api.py"

BEGIN_SENTINEL = "# BEGIN GENERATED CODE"
END_SENTINEL = "# END GENERATED CODE"
