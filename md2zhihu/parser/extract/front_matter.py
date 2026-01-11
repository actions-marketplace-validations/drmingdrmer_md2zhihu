import re
from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple

import yaml

from ...types import RefDict


class FrontMatter(object):
    """
    The font matter is the yaml enclosed between `---` at the top of a markdown.
    """

    def __init__(self, front_matter_text: str) -> None:
        self.text: str = front_matter_text
        self.data: Dict[str, Any] = yaml.safe_load(front_matter_text)

    def get_refs(self, platform: str) -> RefDict:
        """
        Get refs from front matter.
        """
        dic: RefDict = {}

        meta = self.data

        # Collect universal refs
        if "refs" in meta:
            refs = meta["refs"]

            for r in refs:
                dic.update(r)

        # Collect platform specific refs
        if "platform_refs" in meta:
            refs = meta["platform_refs"]
            if platform in refs:
                refs = refs[platform]

                for r in refs:
                    dic.update(r)

        return dic


def extract_front_matter(cont: str) -> Tuple[str, Optional[FrontMatter]]:
    meta: Optional[FrontMatter] = None
    m = re.match(r"^ *--- *\n(.*?)\n---\n", cont, flags=re.DOTALL | re.UNICODE)
    if m:
        cont = cont[m.end() :]
        meta_text = m.groups()[0].strip()
        meta = FrontMatter(meta_text)

    return cont, meta
