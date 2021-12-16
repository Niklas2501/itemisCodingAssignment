import re
from collections import Counter
from typing import Optional

import roman


class GalacticUnitConverter:

    def __init__(self):
        self.roman_digit_to_dec_value = {
            'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000
        }

        self.galactic_digit_to_roman = {}
        self.material_values = {}

    def convert(self) -> None:
        pass

    def process_input_line(self, input_line: str) -> None:
        """
        Receives a single line of user input, executes basic checks and forwards the input based on its type.
        :param input_line: A single line of input as a string.
        :return: None
        """

        # Split the input line into single terms separated by a space.
        parts = input_line.strip().split(' ')

        # Basic check for the number of terms such that out of range errors are avoided.
        if len(parts) < 3:
            print('invalid input. Input ignored.')

        # Pass the list of terms in the input line to a specific sub method based on the input type.
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
        Input line example: pish is X
        :param parts: A list of terms (strings) in the input line.
        :return: None
        """

        if not (len(parts) == 3 and parts[1] == 'is' and self.is_valid_roman_numeral(parts[-1])):
            print('invalid input. Input ignored.')
        else:
            # Store the mapping of galactic to a roman numeral
            self.galactic_digit_to_roman[parts[0]] = parts[-1]

    def handle_material_info(self, parts: [str]) -> None:
        """
        Used to process and store inputs regarding the value of materials.
        Input line example: glob glob Silver is 34 Credits
        :param parts: A list of terms (strings) in the input line.
        :return: None
        """

        # The total number of credits should be an integer at the second to last position.
        try:
            credits = int(parts[-2])
        except ValueError:
            credits = None

        # Abort in case no valid credit amount is given or the input ends with an unexpected term.
        if parts[-1] != 'Credits' or credits is None:
            print('invalid input. Input ignored.')
            return

        # The material should be the fourth to last term, everything before describes the amount as a galactic number.
        material = parts[-4]
        amount_galactic = parts[0:-4]
        amount_roman = self.convert_galactic_to_roman(amount_galactic)

        # amount_roman is None in case amount_galactic can not be converted to a valid roman numeral.
        if amount_roman is None:
            print('invalid input. Input ignored.')
            return

        # A library function is used to convert the amount in roman numeral into a decimal representation.
        amount_decimal = roman.fromRoman(amount_roman)

        # Calculate the and store the value of a single unit of the material.
        material_value = credits // amount_decimal
        self.material_values[material] = material_value

    def convert_galactic_to_roman(self, galactic_digits: [str]) -> Optional[str]:
        """
        Converts a list of galactic digits to a string containing the corresponding roman numeral.
        :param galactic_digits: A list of galactic digits.
        :return: The corresponding roman numeral as a string. In case no valid roman numeral exists None is returned.
        """

        roman_numeral = []

        for galactic_digit in galactic_digits:
            roman_digit = self.galactic_digit_to_roman.get(galactic_digit)
            roman_numeral.append(roman_digit)

        roman_numeral = "".join(roman_numeral)

        if self.is_valid_roman_numeral(roman_numeral):
            return roman_numeral
        else:
            return None

    def handle_request(self, parts: [str]) -> None:
        pass

    def get_smaller_roman_digits(self, target_roman_digit: str) -> list[str]:
        """
        :param target_roman_digit: The roman digit as string for which the ones with lower values should be calculated.
        :return: A list of roman digits for which holds that their value is lower than the one of the target digit
        """

        smaller_digits = []
        value_of_target = self.roman_digit_to_dec_value.get(target_roman_digit)

        # Safe variant which does not rely on the fact the the dictionary is sorted by value.
        for digit, value in self.roman_digit_to_dec_value.items():
            if value < value_of_target:
                smaller_digits.append(digit)

        return smaller_digits

    def rule_compliant_subtraction(self, first_roman_digit: str, second_roman_digit: str) -> bool:
        """
        Checks whether second_numeral - first_numeral is allowed according to the rules.
        :param first_roman_digit: A for a roman numeral (sub)string "AB"
        :param second_roman_digit: B for a roman numeral (sub)string "AB"
        :return: True if second_roman_digit - first_roman_digit is allowed according to the rules, False otherwise.
        """

        # Alternatively to the hard-coded rules for I,X and C, a "subtraction is only allowed from the next
        # two higher symbols" rule could have been implemented using self.numeral_to_value.
        allowed_to_subtract_from = {
            'I': ['V', 'X'],
            'X': ['L', 'C'],
            'C': ['D', 'M'],
        }

        if first_roman_digit in ['V', 'L', 'D']:
            return False
        elif not second_roman_digit in allowed_to_subtract_from.get(first_roman_digit):
            return False
        else:
            return True

    def is_valid_roman_numeral(self, roman_numeral: str) -> bool:
        """
        Checks whether the input string is a valid roman numeral.
        For the purpose of the assignment, the implementation adheres to the given rules,
            even if simpler tests for the correctness of a roman numeral exist.
        :param roman_numeral: A string containing a roman numeral
        :return: True if roman_numeral is a valid roman numeral, False otherwise.
        """

        # Ensure the passed string only contains valid roman numerals
        if not all([char in self.roman_digit_to_dec_value.keys() for char in roman_numeral]):
            return False

        # "D", "L", and "V" can never be repeated. -> occur once at most
        nbr_occurrences_numerals = Counter(roman_numeral)
        for roman_digit in ['D', 'L', 'V']:
            if nbr_occurrences_numerals[roman_digit] > 1:
                return False

        # At most 3 repetitions (+1  in case of subtraction) check
        # Assumption: Cases like XXIX (less than 3 receptions followed by a subtraction) are also valid.
        for roman_digit in ['I', 'X', 'C', 'M']:

            smaller_digits = self.get_smaller_roman_digits(roman_digit)

            if len(smaller_digits) > 0:
                smaller_digits_str = "".join(smaller_digits)
                # Pattern: More than 4 receptions or
                pattern = f'([{roman_digit}]{{4,}}|([{roman_digit}]{{1,3}}[{smaller_digits_str}][{roman_digit}]{{2,}}))'
            else:
                # Specific pattern for roman_digit, from which nothing can be subtracted, e.g. I
                # smaller_digits is emtpy -> wrong pattern check
                pattern = f'[{roman_digit}]{{4,}}'

            # In case the pattern is found a rules is broken and the sanity check fails.
            pattern = re.compile(pattern)
            if bool(re.search(pattern, roman_numeral)):
                return False

        for index, current_digit in enumerate(roman_numeral):

            # No subtraction of first numeral possible
            if index == 0:
                continue

            prev_digit = roman_numeral[index - 1]

            # Subtraction case:
            if self.roman_digit_to_dec_value.get(prev_digit) < self.roman_digit_to_dec_value.get(current_digit):
                if not self.rule_compliant_subtraction(prev_digit, current_digit):
                    return False

                # Starting from the third numeral, a double subtraction error must be checked.
                if index > 1:

                    # Check if numeral at two positions before the current one also has a lower value
                    prev_digit_2 = roman_numeral[index - 2]
                    if self.roman_digit_to_dec_value.get(prev_digit_2) < self.roman_digit_to_dec_value.get(current_digit):
                        return False

        return True


if __name__ == '__main__':
    guc = GalacticUnitConverter()
    guc.convert()
