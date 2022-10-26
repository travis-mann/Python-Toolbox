#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""yaml_gui.py: Creates an interactive gui for yaml files - ideal for config setups"""

__author__ = "Travis Mann"
__version__ = "1.0"
__maintainer__ = "Travis Mann"
__email__ = "tmann.eng@gmail.com"
__status__ = "Production"


# --- imports ---
from yaml_funcs import *
import sys
import yaml
from PyQt5.QtWidgets import (QApplication, QComboBox, QHBoxLayout,
                             QLabel, QRadioButton, QVBoxLayout,
                             QWidget, QButtonGroup, QMainWindow,
                             QPushButton)


# --- glob vars ---
# N/A


# --- classes ---
class YamlGui(QMainWindow):
    """
    purpose: creates a gui for app configs from a specifically formatted yaml file
    """
    def __init__(self, yaml_fl: str) -> None:
        """
        :param yaml_fl: yaml file location
        """
        print('initializing YamlGui class...')
        # inherit from QMainWindow parent class to enable on click events for radio buttons
        super().__init__()

        # ~~ inst attr from params ~~
        self.yaml_fl = yaml_fl

        # ~~ other inst attr ~~
        # set layout and define central widget
        self.layout = QVBoxLayout()  # layout for the central widget
        self.widget = QWidget()  # central widget

        # ~~ main logic ~~
        self.widget.setLayout(self.layout)  # set widget layout
        self.widget.setWindowTitle("My Yaml Gui")
        yaml_dict = self.get_yaml_contents()
        self.layout.addWidget(self.get_choices_widget(yaml_dict))
        self.layout.addWidget(self.get_push_button('Confirm', self.on_click_confirm))

        # add main widget to the app
        self.widget.show()

    def get_yaml_contents(self) -> dict:
        """
        purpose: convert yaml contents into a dict to create gui from
        :return yaml_dict: contents from yaml file
        """
        print('getting yaml contents...')
        # open yaml file and return values as a dict
        with open(self.yaml_fl, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)

    def get_choices_widget(self, yaml_dict: dict) -> QWidget:
        """
        purpose: create a widget with choices configured in self.yaml_fl
        :param yaml_dict: dict extracted from yaml file being gui-ified
        """
        print('creating choices widget...')
        # initialize widget & layout
        choices_widget = QWidget()
        choices_layout = QHBoxLayout()
        choices_widget.setLayout(choices_layout)

        # create multiple columns if there are too many choices
        column_choices_widget = QWidget()
        column_choices_layout = QVBoxLayout()
        column_choices_widget.setLayout(column_choices_layout)
        column_choices_layout.addStretch()  # centers choice groups within columns
        elem_ctr = 0  # track elements in a column

        # create multiple button choices
        for group, choices in yaml_dict.items():
            # create choice group
            button_group = QButtonGroup(choices_widget)
            # add header
            column_choices_layout.addWidget(QLabel(group.title()))
            elem_ctr += 1

            # track first radio button to set default values
            is_first_rb = True

            # add choices
            for idx, (text, value) in enumerate(choices.items()):
                # selection is used to store final choice, it is not a choice itself
                if text == "selection":
                    continue

                # get rb or rb with dropdown widget based on choice config in yaml file
                choice_widget = self.get_choice_widget(group, button_group, text, value, is_first_rb)
                column_choices_layout.addWidget(choice_widget)
                elem_ctr += 1

                # first radio button has been handled by this point
                is_first_rb = False

            # create new column if elements in current column surpass threshold
            if elem_ctr >= 10:
                # add column widget to parent widget
                column_choices_layout.addStretch()
                choices_layout.addWidget(column_choices_widget)
                column_choices_layout.setContentsMargins(0, 0, 0, 0)

                # create new column widget
                column_choices_widget = QWidget()
                column_choices_layout = QVBoxLayout()
                column_choices_widget.setLayout(column_choices_layout)
                elem_ctr = 0  # reset element counter

            # final formatting
            column_choices_layout.addStretch()  # centers choice groups within columns
            choices_layout.addWidget(column_choices_widget)
            column_choices_layout.setContentsMargins(0, 0, 0, 0)  # get rid of widget margins
            choices_layout.setContentsMargins(0, 0, 0, 0)  # get rid of widget margins

        # output
        return choices_widget

    def get_choice_widget(self,
                          group: str,
                          button_group,
                          text: str,
                          value,
                          set_checked: bool = False) -> QWidget:
        """
        purpose: create a widget for a single choice - radio buttons for each choice value and an additional
                 drop down for extra related choices if configured in self.yaml_fl
        """
        # case 1: extra options given, add dropdown next to radio button
        if isinstance(value, dict):
            print(f'adding {text} with a dropdown')
            dd_values = list(value.keys())
            dd_values.remove('value')  # value is the value for this choice, not an extra choice
            dd_values.remove('selection')  # selection is the final selected label, not an option
            return self.get_rb_dd_widget(group, text, dd_values, button_group, set_checked=set_checked)

        # case 2: no sub-options
        else:
            # create radio buttons with relevant choices
            rb = QRadioButton(text)

            # add attr to radio button
            rb.choice_group = group
            rb.choice_text = text

            # add on click event
            rb.toggled.connect(self.on_rb_clicked)
            rb.setChecked(set_checked)

            # add button to layout
            button_group.addButton(rb)  # add button to relevant group
            return rb

    def on_rb_clicked(self):
        """
        purpose: add selection from radio button to yaml file on click
        """
        rb = self.sender()
        if rb.isChecked():
            print(f"RB selection for {rb.choice_group} is {rb.choice_text}")
            write_yaml((rb.choice_group, 'selection'), rb.choice_text, self.yaml_fl)

    def get_rb_dd_widget(self,
                         group_text: str,
                         choice_text: str,
                         dd_text: list,
                         button_group: QButtonGroup,
                         set_checked: bool = False) -> QWidget:
        """
        purpose: create a radio button & drop down menu widget with a horizontal layout
        :param group_text: text next to radio button option
        :param choice_text: label on button group
        :param dd_text: text for dropdown menu
        :param button_group: QButtonGroup to add radio button to
        :param set_checked: sets the radio button to be checked within button group
        :return button_dd_widget: widget with a radio button and dropdown
        """
        print('creating rb_dd widget...')
        # create radio buttons with relevant choices
        rb = QRadioButton(choice_text)  # create radio button
        button_group.addButton(rb)  # add button to relevant group
        # add attr to radio button
        rb.choice_group = group_text
        rb.choice_text = choice_text
        # add on click event
        rb.toggled.connect(self.on_rb_clicked)
        rb.setChecked(set_checked)

        return package_elements([rb, DDMenu(dd_text, group_text, choice_text, self.yaml_fl)])

    @staticmethod
    def get_push_button(text: str, on_click: callable) -> QWidget:
        """
        purpose: add a confirm button which closes the gui
        :return:
        """
        print('creating push button...')
        button = QPushButton(text)  # create push button
        button.clicked.connect(on_click)  # add on click event
        return package_elements([button])

    def on_click_confirm(self):
        """
        purpose: click event to close window for confirm button
        """
        print('closing window')
        self.close()


class DDMenu(QComboBox):
    """
    purpose: extend QComboBox functionality by exposing attr to on
             select events with a drop down menu
    """
    def __init__(self,
                 selections: list,
                 group_text: str,
                 choice_text: str,
                 yaml_fl: str):
        """
        :param selections: text options in drop down list
        :param group_text: label for choice group
        :param choice_text: text for radio button of related choice
        :param yaml_fl: yaml file to write selection to
        """
        # inherit from QComboBox parent class
        super().__init__()

        # instance attr from params
        self.yaml_fl = yaml_fl

        # add items
        self.addItems(selections)
        self.currentIndexChanged.connect(self.on_selection)

        # add attr from params to combobox
        self.group_text = group_text
        self.choice_text = choice_text

        # run selection event on 1st selection
        self.on_selection()

    def on_selection(self):
        """
        purpose: add selection from dropdown to yaml file on selection
        """
        print(f'DD selection for {self.group_text} {self.choice_text} is {self.currentText()}')
        write_yaml((self.group_text, self.choice_text, 'selection'), self.currentText(), self.yaml_fl)


# --- func ---
def package_elements(pyqt_elements: list, layout_style = QHBoxLayout) -> QWidget:
    """
    purpose: package pyqt_element into a widget to be added to a layout
    :param pyqt_element: elements to be packaged into a widget.
    :return widget: widget containing element
    """
    # configure sub-widget layout
    layout = layout_style()  # horizontal layout by default
    layout.setContentsMargins(0, 0, 0, 0)  # get rid of widget margins
    widget = QWidget()  # create sub-widget
    widget.setLayout(layout)  # set subwidget to desired layout

    # add element to sub-widget layout
    for element in pyqt_elements:
        layout.addWidget(element)

    # output
    return widget


# --- main ---
if __name__ == "__main__":
    # create pyqt5 app
    App = QApplication(sys.argv)
    # create gui for yaml file
    YG = YamlGui('example_yaml.yml')
    # start the app
    sys.exit(App.exec())


