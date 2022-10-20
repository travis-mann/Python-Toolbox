#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""yaml_funcs.py: Common functions related to yaml files."""

__author__ = "Travis Mann"
__version__ = "1.0"
__maintainer__ = "Travis Mann"
__email__ = "tmann.eng@gmail.com"
__status__ = "Production"

# --- imports ---
import yaml


# --- funcs ---
def read_yaml(label: str, fl: str):
    """
    purpose: read value from yaml file at file location "fl"
    :param label: param label in yaml file
    :param fl: file location for yaml file
    :return value: value connected to label in yaml file at fl
    """
    # load yaml file
    with open(fl, 'r') as yaml_file:
        values = yaml.safe_load(yaml_file)

    # extract desired value
    try:
        return values[label]
    except KeyError:
        print(f'label {label} doesnt exist in yaml file')
        return None


def write_yaml(label: str, value, fl: str) -> None:
    """
    purpose: write a value to a yaml file for an existing label
    :param label: param label in yaml file
    :param value: value connected to label in yaml file at fl
    :param fl: file location for yaml file
    """
    # load yaml file
    with open(fl, 'r') as yaml_file:
        values = yaml.safe_load(yaml_file)

    # cover blank yaml case
    if values is None:
        values = {}

    # add value to local dict
    try:
        values[label] = value
    except KeyError:
        print(f'label {label} doesnt exist in yaml file')
        return None  # guard clause

    # write back to yaml file
    with open(fl, 'w') as file:
        yaml.dump(values, file)
