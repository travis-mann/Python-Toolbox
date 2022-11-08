#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""yaml_funcs.py: Common functions related to yaml files."""

# --- metadata ---
__author__ = "Travis Mann"
__version__ = "1.0"
__maintainer__ = "Travis Mann"
__email__ = "tmann.eng@gmail.com"
__status__ = "Production"


# --- imports ---
import yaml
from flatten_dict import flatten, unflatten


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


def write_yaml(label, value, fl: str) -> None:
    """
    purpose: write a value to a yaml file for an existing label
    :param label: param label in yaml file, use a tuple of keys for a nested dict
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
        if isinstance(label, str):
            values[label] = value
        elif isinstance(label, tuple):  # handle nested dict
            flat_val = flatten(values)
            flat_val[label] = value
            values = unflatten(flat_val)
    except KeyError:
        print(f'label {label} doesnt exist in yaml file')
        return None  # guard clause

    # write back to yaml file
    with open(fl, 'w') as file:
        yaml.dump(values, file)


def read_selection(label: str, fl: str) -> list:
    """
    purpose: read the selected value(s) from a yaml file formatted for the yaml gui
    :param label: param label in yaml file
    :param fl: file location for yaml file
    :return selection_values: list of choices selected in the gui
    """
    # init lists
    selection_values = []

    # load yaml file
    with open(fl, 'r') as yaml_file:
        yaml_values = yaml.safe_load(yaml_file)

    # loop through nested selections to get all relevant values
    values = yaml_values[label]
    while True:  # will end when a yaml value isn't a dict
        selection_label = values['selection']
        print(selection_label)
        selection_value = values[selection_label]
        print(selection_value)
        if isinstance(selection_value, dict):
            # value key in dict corresponds to the actual value for that choice
            true_selection_value = values[selection_label]['value']
            selection_values.append(true_selection_value)
            values = selection_value  # load full dict for next loop
        else:  # final value reached
            selection_values.append(selection_value)
            return selection_values


# --- testing ---
if __name__ == "__main__":
    pass
