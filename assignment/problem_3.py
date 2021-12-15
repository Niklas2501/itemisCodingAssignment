import re
from collections import Counter


class GalacticUnitConverter:

    def __init__(self):
        self.numeral_to_value = {
            'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000
        }

    def convert(self):
        pass

    def read_user_input(self):
        pass

    def handle_user_input(self):
        pass

    def output_results(self):
        pass

    def convert_roman_to_decimal(self, roman_numerals: str):
        pass

    def convert_decimal_to_roman(self, decimal: int):
        pass

    def get_smaller_numerals(self, target_numeral: str):
        """
        :param target_numeral: The roman numeral as string for which the ones with lower values should be calculated.
        :return: A list of roman numerals for which holds that their value is lower than the one of the target numeral
        """

        smaller_numerals = []
        value_of_target = self.numeral_to_value.get(target_numeral)

        # Safe variant which does not rely on the fact the the dictionary is sorted by value.
        for numeral, value in self.numeral_to_value.items():
            if value < value_of_target:
                smaller_numerals.append(numeral)

        return smaller_numerals

    def sanity_check_roman_numerals(self, roman_numerals: str):

        # Ensure the passed string only contains valid roman numerals
        if not all([char in self.numeral_to_value.keys() for char in roman_numerals]):
            return False

        # "D", "L", and "V" can never be repeated. -> occur once at most
        nbr_occurrences_numerals = Counter(roman_numerals)
        for numeral in ['D', 'L', 'V']:
            if nbr_occurrences_numerals[numeral] > 1:
                return False

        # At most 3 repetitions (+1  in case of subtraction) check
        # Assumption: Cases like XXIX (less than 3 receptions followed by a subtraction) are also valid.
        for numeral in ['I', 'X', 'C', 'M']:

            smaller_numerals = self.get_smaller_numerals(numeral)

            if len(smaller_numerals) > 0:
                smaller_numerals_str = "".join(smaller_numerals)
                # Pattern: More than 4 receptions or
                pattern = f'([{numeral}]{{4,}}|([{numeral}]{{1,3}}[{smaller_numerals_str}][{numeral}]{{2,}}))'
            else:
                # Specific pattern for numeral, from which nothing can be subtracted, e.g. I
                # smaller_numerals is emtpy -> wrong pattern check
                pattern = f'[{numeral}]{{4,}}'

            # In case the pattern is found a rules is broken and the sanity check fails.
            pattern = re.compile(pattern)
            if bool(re.search(pattern, roman_numerals)):
                return False




        return True


if __name__ == '__main__':
    guc = GalacticUnitConverter()
    guc.convert()
