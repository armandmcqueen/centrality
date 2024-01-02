import subprocess
from rich import print
from pathlib import Path


def sh(cmd):
    subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)


def main():
    repo_root = Path(__file__).parent.parent
    print(f"Generating SDKs in {repo_root}")

    # Generate the OpenAPI spec
    controlplane_repo = repo_root / "controlplane"
    sh(
        f"make -C {controlplane_repo} gen-openapi-spec"
    )  # TODO: Move this logic out of the makefile?
    # This saves the spec to common/common/sdks/controlplane/openapi.json
