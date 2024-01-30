# Disk Throughput fixes
from pathlib import Path
from typing import Optional

import git
import libcst as cst
from rich import print, inspect
from redbaron import RedBaron

root = Path(git.Repo(".", search_parent_directories=True).working_tree_dir)

MODEL_DEF_PATH = root / "sdk_controlplane/centrality_controlplane_sdk/models/disk_throughput_measurement.py"
# MODEL_DEF_PATH = root / "sdk_example.py"
DATA_API_PATH = root / "sdk_controlplane/centrality_controlplane_sdk/api/data_api.py"


from libcst import matchers as m

class TypeHintTransformer(cst.CSTTransformer):
    def leave_AnnAssign(self, original_node, updated_node):
        # Define a matcher for the specific attribute
        throughput_matcher = m.AnnAssign(
            target=m.Name("throughput"),
            annotation=m.Annotation(m.Subscript(value=m.Name("Optional"), slice=[m.SubscriptElement()])),
        )

        # Check if the node matches the desired pattern
        inspect(original_node.annotation)
        if m.matches(updated_node, throughput_matcher):
            new_annotation = cst.Annotation(annotation=cst.Subscript(
                value=cst.Name(value='dict'),
                slice=[
                    # cst.SubscriptElement(slice=cst.SimpleString(value="'str'")),
                    cst.SubscriptElement(slice=cst.Index(value=cst.SimpleString('"str"'))),
                    cst.SubscriptElement(slice=cst.Index(value=cst.Name(value='DiskThroughput')))
                ]
            ))
            inspect(new_annotation)
            print(new_annotation.code)
            return updated_node.with_changes(annotation=new_annotation)
        return updated_node


# def fix_model_def():
#     # Pydantic subclass implementation, DiskThroughputMeasurement
#     # throughput: Optional[Any], needs to be converted to Dict[str, DiskThroughput]
#     # DiskThroughput needs to be imported from centrality_controlplane_sdk.models.disk_throughput
#
#     # In to_dict, the code that checks if throughput is none should be removed (not 100% necessary I think)
#
#     # In from_dict, the creation of the object needs to be changed so that (1) throughput is actually included and (2) throughput is recursively converted to DiskThroughputs
#
#     module = cst.parse_module(MODEL_DEF_PATH.read_text())
#
#     # print(module.body)
#
#     transformer = TypeHintTransformer()
#     modified_code = module.visit(transformer)
#     print(modified_code.code)

def fix_model_def():
    # Load the model definition code into a RedBaron tree
    red = RedBaron(MODEL_DEF_PATH.read_text())

    ####################################################################################################
    # Add the type alias
    location = 15  # hardcoded
    type_alias = RedBaron("DiskName = str\n")[0]
    red.insert(location, type_alias)

    ####################################################################################################
    # Find the 'throughput' node in the 'DiskThroughputMeasurement' class
    throughput_node = red.find('class', name='DiskThroughputMeasurement').find('name', value='throughput').parent

    # Modify the annotation
    if throughput_node and throughput_node.type == 'assignment':
        # print("found it")
        throughput_node.annotation = "dict[DiskName, DiskThroughput]"

    ####################################################################################################
    # Change from_dict to include the throughput during object creation
    """
    _obj = cls.model_validate({
        "machine_id": obj.get("machine_id"),
        "ts": obj.get("ts"),
    })
    """

    # Find the model_validate function
    func_node = red.find('class', name='DiskThroughputMeasurement').find('def', name='from_dict')
    print(func_node)
    node = func_node.find_all('name', value='model_validate')[1].parent
    dict_node = node.find("call_argument").value
    """
    dict_node is 
    
    {
            "machine_id": obj.get("machine_id"),
            "ts": obj.get("ts"),
        }

    """
    # Add the throughput
    throughput_node = RedBaron(""" 
    "throughput": {
                disk_name: DiskThroughput.from_dict(disk_throughput) 
                for disk_name, disk_throughput 
                in obj.get("throughput").items()
            }
    """)

    dict_node.append(throughput_node)
    inspect(dict_node)
    print(dict_node)


    ####################################################################################################
    # Output the modified code
    print("```python")
    print(red.dumps())
    print("```")
    # TODO: Write this back to the original code file
    # Write the modified code back to the file
    MODEL_DEF_PATH.write_text(red.dumps())

    ####################################################################################################
    # Modify the data api
    red = RedBaron(DATA_API_PATH.read_text())

    ####################################################################################################
    # Change the type annotation for get_metrics (get_latest_metrics is fine)
    node = red.find('class', name='DataApi').find('def', name='get_disk_throughput_metrics')
    print(node)
    # Get the return type annotation node
    # return_type_node = node.find('return_annotation')
    node.return_annotation = "Dict[str, list[DiskThroughputMeasurement]]"
    print(node.return_annotation)
    print(node)

    ####################################################################################################
    # Find and change the return type map
    """
            _response_types_map: Dict[str, Optional[str]] = {
            '200': "Dict[str, object]",
            '422': "HTTPValidationError"
            
        }
    """
    type_map_node = node.find('name', value='_response_types_map').parent.value
    print(type_map_node.value[0].value)
    type_map_node.value[0].value = '"Dict[str, list[DiskThroughputMeasurement]]"'
    print(type_map_node)

    # TODO: Repeat this for the other variants
    # Write the modified code back to the file
    DATA_API_PATH.write_text(red.dumps())



if __name__ == '__main__':
    fix_model_def()




