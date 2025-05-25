""" """

import yaml


class FlowListDumper(yaml.SafeDumper):
    """ """

    def represent_sequence(self, tag, sequence):
        return super().represent_sequence(tag, sequence, flow_style=True)
