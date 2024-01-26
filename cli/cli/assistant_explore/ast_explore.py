from typing import Optional, Union
import ast
import graphviz
from rich import print, inspect
import typer
from pathlib import Path

app = typer.Typer()


def build_ast_graph(
    node: Union[ast.AST, list, None],
    graph: graphviz.Digraph,
    parent: Optional[str] = None,
    edge_label: str = "",
) -> None:
    """
    Recursively build a graph from the AST node.

    Args:
    node (Union[ast.AST, list, None]): The current AST node or list of nodes.
    graph (graphviz.Digraph): The Graphviz Digraph object to build the graph.
    parent (Optional[str]): Label of the parent node in the graph.
    edge_label (str): Label for the edge connecting the node to its parent.
    """
    if isinstance(node, list):
        for item in node:
            build_ast_graph(item, graph, parent, edge_label)
    elif isinstance(node, ast.AST):
        node_label = f'{type(node).__name__} ({getattr(node, "lineno", "")}:{getattr(node, "col_offset", "")})'
        graph.node(node_label)
        if parent:
            graph.edge(parent, node_label, label=edge_label)

        for field, value in ast.iter_fields(node):
            build_ast_graph(value, graph, node_label, field)


def visualize_ast(source_code: str) -> str:
    """
    Visualize the AST of the given source code.

    Args:
    source_code (str): A string of Python source code.

    Returns:
    str: The filename of the generated graph.
    """
    tree = ast.parse(source_code)
    inspect(tree)
    # inspect(tree.body[6])
    # inspect(tree.body[6].targets[0])
    # configuration_function_call = tree.body[6].value
    # # inspect(tree.body[6].value)
    # inspect(configuration_function_call.func)
    class_defs = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    subclass_class_defs = [
        class_def
        for class_def in class_defs
        if class_def.name != "DataVisualizer"
        and len(class_def.bases) == 1
        and class_def.bases[0].id == "DataVisualizer"
    ]
    assert (
        len(subclass_class_defs) == 1
    ), f"Expected exactly one subclass of DataVisualizer, got {len(subclass_class_defs)}: {subclass_class_defs}"
    subclass_class_def = subclass_class_defs[0]
    collect_data_function_def = None
    visualize_data_function_def = None
    for node in ast.walk(subclass_class_def):
        if isinstance(node, ast.FunctionDef):
            print(node.name)
            inspect(node)
            if node.name == "collect_data":
                collect_data_function_def = node

            if node.name == "visualize_data":
                visualize_data_function_def = node

    assert (
        collect_data_function_def is not None
    ), f"Could not find collect_data function definition in subclass {subclass_class_def.name}"
    assert (
        visualize_data_function_def is not None
    ), f"Could not find visualize_data function definition in subclass {subclass_class_def.name}"

    inspect(collect_data_function_def.returns)
    print(ast.dump(collect_data_function_def, indent=4))

    return ""
    graph = graphviz.Digraph(format="png")
    build_ast_graph(tree, graph)
    output_filename = "ast-graph"
    graph.render(output_filename, cleanup=True)
    return output_filename


@app.command()
def main(file: str):
    source_file = Path(file)
    with source_file.open() as f:
        source_code = f.read()

    output_file = visualize_ast(source_code)
    print(f"AST visualization saved as: {output_file}")


if __name__ == "__main__":
    app()
