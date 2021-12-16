import re
from collections import Counter

import roman


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

        self.galactic_to_roman = {}
        self.material_values = {}

    def convert(self) -> None:
        pass

    def process_input_line(self, input_line: str) -> None:
        """
        Receives a single line of user input, executes basic checks and forwards the input based on its type.
        :param input_line: A single line of input as a string.
        :return: None
        """

        parts = input_line.strip().split(' ')

        if len(parts) < 3:
            print('invalid input. Input ignored.')

        if parts[-1] == '?':
            self.handle_request(parts)
        elif parts[-1] == 'Credits':
            self.handle_material_info(parts)
        elif parts[1] == 'is' and self.is_valid_roman_numeral(parts[-1]):
            self.handle_galactic_numeral_info(parts)
        else:
            print('invalid input. Input ignored.')

    def handle_galactic_numeral_info(self, parts: [str]) -> None:
        """
        Used to process and store inputs regarding the mapping of intergalactic to roman numerals.
        :param parts: A list of terms (strings) in the input line.
        :return: None
        """

        if not (len(parts) == 3 and parts[1] == 'is' and self.is_valid_roman_numeral(parts[-1])):
            print('invalid input. Input ignored.')
        else:
            self.galactic_to_roman[parts[0]] = parts[-1]

    def handle_material_info(self, parts: [str]) -> None:

        try:
            credits = int(parts[-2])
        except ValueError:
            credits = None

        material = parts[-4]
        amount_galactic = parts[0:-4]
        amount_roman = []

        for galactic_numeral in amount_galactic:
            roman_numeral = self.galactic_to_roman.get(galactic_numeral)
            amount_roman.append(roman_numeral)

        amount_roman = "".join(amount_roman)

        if parts[-1] != 'Credits' or credits is None or not self.is_valid_roman_numeral(amount_roman):
            print('invalid input. Input ignored.')
            return

        # A library function is used to convert the amount in roman numeral into a decimal representation.
        amount_decimal = roman.fromRoman(amount_roman)
        material_value = credits // amount_decimal
        self.material_values[material] = material_value

    def handle_request(self, parts: [str]) -> None:
        pass

    def get_smaller_r_numerals(self, target_r_numeral: str) -> list[str]:
        """
        :param target_r_numeral: The roman numeral as string for which the ones with lower values should be calculated.
        :return: A list of roman numerals for which holds that their value is lower than the one of the target numeral
        """

        smaller_numerals = []
        value_of_target = self.numeral_to_value.get(target_r_numeral)

        # Safe variant which does not rely on the fact the the dictionary is sorted by value.
        for numeral, value in self.numeral_to_value.items():
            if value < value_of_target:
                smaller_numerals.append(numeral)

        return smaller_numerals

    def rule_compliant_subtraction(self, first_r_numeral: str, second_r_numeral: str) -> bool:
        """
        Checks whether second_numeral - first_numeral is allowed according to the rules.
        :param first_r_numeral: A for a roman numeral (sub)string "AB"
        :param second_r_numeral: B for a roman numeral (sub)string "AB"
        :return: True if second_numeral - first_numeral is allowed according to the rules, else False.
        """

        # Alternatively to the hard-coded rules for I,X and C, a "subtraction is only allowed from the next
        # two higher symbols" rule could have been implemented using self.numeral_to_value.
        allowed_to_subtract_from = {
            'I': ['V', 'X'],
            'X': ['L', 'C'],
            'C': ['D', 'M'],
        }

        if first_r_numeral in ['V', 'L', 'D']:
            return False
        elif not second_r_numeral in allowed_to_subtract_from.get(first_r_numeral):
            return False
        else:
            return True

    def is_valid_roman_numeral(self, roman_numerals: str) -> bool:
        """
        Checks whether the input string is a valid roman numeral.
        For the purpose of the assignment, the implementation adheres to the given rules,
            even if a simpler test for the correctness of Roman numerals exists.
        :param roman_numerals: A string containing a roman numeral
        :return: True if roman_numerals is a valid roman number, False otherwise.
        """

        # Ensure the passed string only contains valid roman numerals
        if not all([char in self.numeral_to_value.keys() for char in roman_numerals]):
            return False

        # "D", "L", and "V" can never be repeated. -> occur once at most
        nbr_occurrences_numerals = Counter(roman_numerals)
        for r_numeral in ['D', 'L', 'V']:
            if nbr_occurrences_numerals[r_numeral] > 1:
                return False

        # At most 3 repetitions (+1  in case of subtraction) check
        # Assumption: Cases like XXIX (less than 3 receptions followed by a subtraction) are also valid.
        for r_numeral in ['I', 'X', 'C', 'M']:

            smaller_numerals = self.get_smaller_r_numerals(r_numeral)

            if len(smaller_numerals) > 0:
                smaller_numerals_str = "".join(smaller_numerals)
                # Pattern: More than 4 receptions or
                pattern = f'([{r_numeral}]{{4,}}|([{r_numeral}]{{1,3}}[{smaller_numerals_str}][{r_numeral}]{{2,}}))'
            else:
                # Specific pattern for r_numeral, from which nothing can be subtracted, e.g. I
                # smaller_numerals is emtpy -> wrong pattern check
                pattern = f'[{r_numeral}]{{4,}}'

            # In case the pattern is found a rules is broken and the sanity check fails.
            pattern = re.compile(pattern)
            if bool(re.search(pattern, roman_numerals)):
                return False

        for index, current_r_numeral in enumerate(roman_numerals):

            # No subtraction of first numeral possible
            if index == 0:
                continue

            prev_r_numeral = roman_numerals[index - 1]

            # Subtraction case:
            if self.numeral_to_value.get(prev_r_numeral) < self.numeral_to_value.get(current_r_numeral):
                if not self.rule_compliant_subtraction(prev_r_numeral, current_r_numeral):
                    return False

                # Starting from the third numeral, a double subtraction error must be checked.
                if index > 1:

                    # Check if numeral at two positions before the current one also has a lower value
                    prev_r_numeral_2 = roman_numerals[index - 2]
                    if self.numeral_to_value.get(prev_r_numeral_2) < self.numeral_to_value.get(current_r_numeral):
                        return False

        return True


if __name__ == '__main__':
    guc = GalacticUnitConverter()
    guc.convert()
