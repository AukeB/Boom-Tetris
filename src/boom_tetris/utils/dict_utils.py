""" """

from typing import Union, Any
from ruamel.yaml.comments import CommentedMap, CommentedSeq


def format_for_writing_to_yaml_file(
    obj: Union[dict, list, Any], path=None
) -> Union[CommentedMap, CommentedSeq, Any]:
    """ """
    path = path or []

    if isinstance(obj, dict):
        new_map = CommentedMap()
        for k, v in obj.items():
            new_map[k] = format_for_writing_to_yaml_file(v, path + [k])
        return new_map

    elif isinstance(obj, list):
        # Special case for POLYOMINO.ALL_SHAPES:
        if path == ["POLYOMINO", "ALL_SHAPES"]:
            outer = CommentedSeq()
            for shape in obj:
                inner = CommentedSeq()
                inner.fa.set_flow_style()  # force inline for each 2D shape
                for point in shape:
                    inner.append(point)
                outer.append(inner)
            return outer

        seq = CommentedSeq()
        for item in obj:
            seq.append(format_for_writing_to_yaml_file(item, path))
        seq.fa.set_flow_style()  # Force inline.
        return seq

    else:
        return obj


class DotDict(dict):
    """ """

    def __init__(self, data=None):
        """ """
        super().__init__()
        data = data or {}

        for key, value in data.items():
            self[key] = self._wrap(value)

    def __getattr__(self, attr):
        """ """
        try:
            return self[attr]
        except KeyError as e:
            raise AttributeError(f"'DotDict' object has no attribute '{attr}'") from e

    def __setattr__(self, key, value):
        """ """
        self[key] = self._wrap(value)

    def __delattr__(self, key):
        """ """
        try:
            del self[key]
        except KeyError as e:
            raise AttributeError(f"'DotDict' object has no attribute '{key}'") from e

    def _wrap(self, value):
        """ """
        if isinstance(value, dict):
            return DotDict(value)
        elif isinstance(value, list):
            return [self._wrap(v) for v in value]
        return value

    def to_dict(self) -> dict:
        """ """
        result = {}

        for key, value in self.items():
            if isinstance(value, DotDict):
                result[key] = value.to_dict()
            elif isinstance(value, list):
                result[key] = [
                    item.to_dict() if isinstance(item, DotDict) else item
                    for item in value
                ]
            else:
                result[key] = value

        return result
