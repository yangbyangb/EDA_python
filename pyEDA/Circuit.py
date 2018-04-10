import math
import numpy as np

from . import Element


class Circuit(list):

    def __init__(self, title, filename=None):
        self.title = title
        self.filename = filename
        self.nodes_dict = {}
        self.gnd = '0'
        self.nodes = 0

    def create_node(self, name):
        index = 0 in self.nodes_dict
        if name not in self.nodes_dict:
            if name == '0':
                node = 0
            else:
                node = int(len(self.nodes_dict) / 2) + (not index)
            self.nodes_dict.update({node: name})
            self.nodes_dict.update({name: node})

        return name

    def add_node(self, name):
        if name not in self.nodes_dict:
            if name == '0':
                node = 0
            else:
                index = 0 in self.nodes_dict
                node = int(len(self.nodes_dict) / 2) + (not index)
            self.nodes_dict.update({node: name})
            self.nodes_dict.update({name: node})
        else:
            node = self.nodes_dict[name]
        return node

    def is_nonlinear(self):
        for elem in self:
            if elem.is_nonlinear:
                return True
        return False
