import re
from typing import Optional

from ...types import ASTNodes
from ...types import RefDict


def replace_ref_with_def(nodes: ASTNodes, refs: RefDict, do_replace: bool) -> RefDict:
    """
    Convert ``[text][link-def]`` to ``[text](link-url)``
    Convert ``[link-def][]``     to ``[link-def](link-url)``
    Convert ``[link-def]``       to ``[link-def](link-url)``

    If `do_replace` is True, replace the ref with def.
    Otherwise, just extract the used refs.
    """

    used_defs: RefDict = {}

    for n in nodes:
        if "children" in n:
            used = replace_ref_with_def(n["children"], refs, do_replace)
            used_defs.update(used)

        if n["type"] != "text":
            continue

        t: str = n["text"]
        link = re.match(r"^\[(.*?)\](\[([^\]]*?)\])?$", t)
        if not link:
            continue

        gs = link.groups()
        txt: str = gs[0]
        definition: Optional[str] = None
        if len(gs) >= 3:
            definition = gs[2]

        if definition is None or definition == "":
            definition = txt

        if definition in refs:
            r = refs[definition]
            used_defs[definition] = r

            if do_replace:
                n["type"] = "link"
                #  TODO title
                n["link"] = r.split()[0]
                n["children"] = [{"type": "text", "text": txt}]

    return used_defs
