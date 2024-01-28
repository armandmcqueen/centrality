# Disk Throughput fixes
from pathlib import Path
from typing import Optional

import git
import libcst as cst
from rich import print, inspect

root = Path(git.Repo(".", search_parent_directories=True).working_tree_dir)

MODEL_DEF_PATH = root / "sdk_controlplane/centrality_controlplane_sdk/models/disk_throughput_measurement.py"
DATA_API_PATH = root / "sdk_controlplane/centrality_controlplane_sdk/api/data_api.py"



class DiskThroughputMeasurementTransformer(cst.CSTTransformer):
    """ Change the type of DiskThroughputMeasurement.throughput from Optional[Any] to Dict[str, DiskThroughput] """

    def visit_ClassDef(self, node: cst.ClassDef) -> Optional[bool]:
        if node.name.value == "DiskThroughputMeasurement":
            assert len(node.bases) == 1, "Expected DiskThroughputMeasurement to have exactly one base class"
            assert node.bases[0].value.value == "BaseModel", f"Expected DiskThroughputMeasurement to have BaseModel as its base class, got {node.bases[0].value.value}"
            print("Found DiskThroughputMeasurement")
            print(type(node.body))
            class_statements = node.body.body
            for e in class_statements:
                if not isinstance(e, cst.SimpleStatementLine):
                    print(type(e))
        return None


def fix_model_def():
    # Pydantic subclass implementation, DiskThroughputMeasurement
    # throughput: Optional[Any], needs to be converted to Dict[str, DiskThroughput]
    # DiskThroughput needs to be imported from centrality_controlplane_sdk.models.disk_throughput

    # In to_dict, the code that checks if throughput is none should be removed (not 100% necessary I think)

    # In from_dict, the creation of the object needs to be changed so that (1) throughput is actually included and (2) throughput is recursively converted to DiskThroughputs

    module = cst.parse_module(MODEL_DEF_PATH.read_text())

    # print(module.body)

    transformer = DiskThroughputMeasurementTransformer()
    module.visit(transformer)

if __name__ == '__main__':
    fix_model_def()




