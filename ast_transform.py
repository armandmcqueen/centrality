# Disk Throughput fixes
from pathlib import Path
from typing import Optional

import git
from rich import print, inspect
from redbaron import RedBaron

root = Path(git.Repo(".", search_parent_directories=True).working_tree_dir)

MODEL_DEF_PATH = root / "sdk_controlplane/centrality_controlplane_sdk/models/disk_throughput_measurement.py"
DATA_API_PATH = root / "sdk_controlplane/centrality_controlplane_sdk/api/data_api.py"




def fix_model_def():
    # Load the model definition code into a RedBaron tree
    red = RedBaron(MODEL_DEF_PATH.read_text())

    ####################################################################################################
    # Add the type alias
    location = 15  # hardcoded
    type_alias = RedBaron("DiskName = str\n")[0]
    red.insert(location, type_alias)

    import_node = RedBaron("from centrality_controlplane_sdk.models.disk_throughput import DiskThroughput\n")[0]
    red.insert(location, import_node)

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
    # TODO: This fails, we need to leave the map as is, and then manually convert the output into the correct type
    """
    current code
    
    
    response_data.read()
    return self.api_client.response_deserialize(
        response_data=response_data,
        response_types_map=_response_types_map,
    ).data
    """

    """
    desired
    
    dict_return = self.api_client.response_deserialize(
        response_data=response_data,
        response_types_map=_response_types_map,
    ).data
    structured_output = {
        machine_id: [DiskThroughputMeasurement(**x) for x in measurements]
        for machine_id, measurements in dict_return.items()
    }
    return structured_output
    """
    # Convert the return into an assignment to dict_return

    # Get the return node
    return_node = node.find("return")

    # Create the new assignment node
    assignment_node = RedBaron("dict_return = None")[0]
    assignment_node.value = return_node.value
    # print(node)
    return_node.replace(assignment_node)
    print("value", node.value)

    # Add the structured output node
    # TODO: This doesn't have correct indentation, but it isn't syntactically incorrect
    structured_output_node = RedBaron("""
    structured_output = {
        machine_id: [DiskThroughputMeasurement(**x) for x in measurements]
        for machine_id, measurements in dict_return.items()
    }
    """)
    # print(structured_output_node)
    node.value.append(structured_output_node)
    print("value2", node.value)

    # Add the return node
    new_return_node = RedBaron("return structured_output")[0]
    node.append(new_return_node)

    print(node)

    # TODO: Repeat this for the other variants. Or just delete the variants?
    # Write the modified code back to the file
    DATA_API_PATH.write_text(red.dumps())



if __name__ == '__main__':
    fix_model_def()




