""" """


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
