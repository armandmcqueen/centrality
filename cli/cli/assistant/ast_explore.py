from typing import Optional, Union
import ast
import graphviz
from rich import print, inspect


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
    graph = graphviz.Digraph(format="png")
    build_ast_graph(tree, graph)
    output_filename = "ast-graph.png"
    graph.render(output_filename, cleanup=True)
    return output_filename


if __name__ == "__main__":
    # Example usage
    source_code = """
    def greet(name):
        print(f"Hello, {name}!")
    """

    output_file = visualize_ast(source_code)
    print(f"AST visualization saved as: {output_file}")
