"""
Translate sheets and field names.

This class handle the translation from english to hebrew.
"""

import json
import sys
import os


class i18n(object):
    """
    i18n handler.

    Translating the fields and sheets names.
    """

    fields = {}
    sheets = {}

    def __init__(self):
        """Constructing."""
        self.fields = self.__read_json_file('fields.json')
        self.sheets = self.__read_json_file('sheets.json')

    def __read_json_file(self, file):
        """
        Reding a file content.

        :param file:
            The name of the file we need to read.
        """
        file = open(os.path.dirname(os.path.abspath(__file__))
                    + "/assets/" + file, "r")

        return json.load(file)

    def set_fields(self, fields):
        """
        Set the fields.

        When you need to set different values for the fields translation you
        can use this method.

        :param fields:
            The new fields to set.
        """
        self.fields = fields

    def translate_field(self, field):
        """
        Translate a given field form english to hebrew.

        :param field:
            The field name for translation.
        """
        if field in self.fields.keys():
            return self.fields[field]

        return None

    def set_sheets(self, sheets):
        """
        Set the sheets.

        When you need to set different values for the sheets translation you
        can use this method.

        :param fields:
            The new sheets to set.
        """
        self.sheets = sheets

    def translate_sheet(self, sheet):
        """
        Translate a given sheet form english to hebrew.

        :param field:
            The field name for translation.
        """
        if sheet in self.sheets.keys():
            return self.sheets[sheet]

        return None
