import hashlib
import json


def md5hex(item: str) -> str:
    """Create md5hex from a string"""

    to_md5 = item.encode()

    return hashlib.md5(to_md5, usedforsecurity=False).hexdigest()


def md5hex_from_json(item: dict[str, str]) -> str:
    """Create MD5 hex from a dictionary"""

    body = json.dumps(item, sort_keys=True)
    return md5hex(body)
