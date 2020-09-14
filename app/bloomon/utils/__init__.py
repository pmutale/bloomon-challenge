import logging
import re
from argparse import Namespace
from collections import Counter

import pandas as pd
import numpy as np
from simple_colors import *

from app.bloomon import exceptions

logger = logging.getLogger(__name__)

flower_regex = r"^[a-z][A-Z]$"
design_regex = r"^[A-Z][SL]\d*[a-z]\d*[a-z]\d*[a-z]\d*$"


class BouquetData:
    def __init__(self, name, size, quantity, specifications, flowers):
        self.name = name
        self.size = size
        self.quantity = quantity
        self.specifications = specifications
        self.flowers = flowers


class ExtractedInput:
    sep = "\n"

    def __init__(self, design, flowers):
        self.design = design
        self.flowers = flowers

    @staticmethod
    def validate(list_elements, regex):
        """
        Validate against a specific format for elements in question
        :param list_elements: List()
        :param regex: Regular expression
        :return:
        """
        result = []
        for item in list_elements:
            if item and not re.match(regex, item):
                raise exceptions.ValidateFormatException(
                    f"The given bouquet design or flower type in: {magenta(item, 'bold')} does not conform to given format. Please read the header information!"
                )
            # Skip empty Elements
            if item:
                result.append(item)
        return result

    def get_design(self):
        """ Retrieve and validate  Bouquet design input elements"""
        if not self.design:
            raise exceptions.EmptyDetailsException(
                "None or insufficient details about bouquet were given"
            )
        return self.validate(self.design.split(self.sep), design_regex)

    def get_flowers(self):
        """ Retrieve and validate Bouquet flowers input elements"""
        if not self.flowers:
            raise exceptions.EmptyDetailsException(
                "None or insufficient flower details were given"
            )
        return self.validate(self.flowers.split(self.sep), flower_regex)

    @staticmethod
    def _get_name_and_size_of_bouquet(design):
        """Get name and size of bouquets supplied"""
        return list("".join(re.findall(r"[A-Z].?", design)))

    @staticmethod
    def _get_total_quantity(design):
        """Get Total quantity of flowers in bouquet"""
        return "".join(re.findall(r"\d+$", design))

    @staticmethod
    def _get_flowers_specie_quantity(design, size):
        """Get all flowers specie and quantity being supplied"""
        return {
            "".join([x[-1], size]): int(x[:-1]) for x in re.findall(r"\d*(?:[a-z])", design)
        }

    def extracted_input_data(self):
        for design in self.get_design():
            name, size = self._get_name_and_size_of_bouquet(design)
            flowers = Counter([flower for flower in self.flowers.split("\n") if flower])
            return BouquetData(
                name,
                size,
                int(self._get_total_quantity(design)),
                self._get_flowers_specie_quantity(design, size),
                dict(sorted(flowers.most_common())),
            )


class BouquetService:
    def __init__(self, bouquet):
        self.bouquet = bouquet

    def apply(self):
        flowers = list(
            (pd.DataFrame([self.bouquet.flowers]) / pd.DataFrame([self.bouquet.specifications])
             ).fillna(0).apply(int))
        output = f"{self.bouquet.name}{self.bouquet.size}{self._get_flower_details(flowers)}"
        for _ in range(max(flowers)):
            print(output)
            return output

        if not any(flowers):
            # Print available bouquets there are not enough flowers to create a standard design
            print(output)
            return output

    def _get_flower_details(self, flowers):
        full_blossoms = self._stringify_given_data(self.bouquet.specifications)
        if any(flowers):
            for _ in range(min(flowers, key=lambda x: x == 0)):
                return full_blossoms
        else:
            return self._stringify_given_data(self.bouquet.flowers)

    @staticmethod
    def _stringify_given_data(data):
        return ''.join(
                    ["{specie}{amount}".format(specie=specie, amount=amount) for specie, amount in {
                        list(key)[0]: value for key, value in data.items()
                    }.items()]
                )
