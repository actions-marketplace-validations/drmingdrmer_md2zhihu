import re

from ...renderer import MDRender
from ...renderer import RenderNode
from ...types import ASTNode
from ...types import ASTNodes
from ..mistune_parser import new_parser


def parse_in_list_tables(nodes: ASTNodes) -> ASTNodes:
    """
    mistune does not parse table in list item.
    We need to recursively fix it.
    """

    rst: ASTNodes = []
    for n in nodes:
        if "children" in n:
            n["children"] = parse_in_list_tables(n["children"])

        new_nodes = convert_paragraph_table(n)
        rst.extend(new_nodes)

    return rst


def convert_paragraph_table(node: ASTNode) -> ASTNodes:
    """
    Parse table text in a paragraph and returns the ast of parsed table.

    :return: a list of ast nodes.
    """

    if node["type"] != "paragraph":
        return [node]

    children = node["children"]

    if len(children) == 0:
        return [node]

    c0 = children[0]
    if c0["type"] != "text":
        return [node]

    txt: str = c0["text"]

    table_reg = r" {0,3}\|(.+)\n *\|( *[-:]+[-| :]*)\n((?: *\|.*(?:\n|$))*)\n*"

    match = re.match(table_reg, txt)
    if match:
        mdr = MDRender(None, features={})
        partialmd_lines = mdr.render(RenderNode(node))
        partialmd = "".join(partialmd_lines)

        parser = new_parser()
        new_children: ASTNodes = parser(partialmd)

        return new_children
    else:
        return [node]
