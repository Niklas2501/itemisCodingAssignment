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
        """
        Main method of the convert which just waits for input and forwards it to the processing of individual lines.
        :return: None
        """

        while True:
            try:
                input_line = input()
            except (KeyboardInterrupt, EOFError):
                # Clean exit on termination
                break

            if input_line == '':
                break
            else:
                self.process_input_line(input_line)

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
            return

        # Pass the list of terms in the input line to a specific sub method based on the input type.
        if parts[-1] == '?':
            self.handle_request(parts)
        elif parts[-1] == 'Credits':
            self.handle_material_info(parts)
        elif parts[1] == 'is' and self.is_valid_roman_numeral(parts[-1]):
            self.handle_galactic_numeral_info(parts)
        else:
            print('invalid input. Input ignored.')

    def handle_galactic_numeral_info(self, parts: list[str]) -> None:
        """
        Used to process and store inputs regarding the mapping of intergalactic to roman numerals.
        Input line example: pish is X
        :param parts: A list of terms (strings) in the input line.
        :return: None
        """

        if not (len(parts) == 3 and parts[1] == 'is' and self.is_valid_roman_numeral(parts[-1])):
            print('invalid input. Input ignored.')
        else:
            galactic_digit, roman_digit = parts[0], parts[-1]

            # Ensure the last part of the input really is a roman digit
            if roman_digit in self.roman_digit_to_dec_value.keys():
                # Store the mapping of galactic to a roman numeral
                self.galactic_digit_to_roman[galactic_digit] = roman_digit
            else:
                print('invalid input. Input ignored.')

    def handle_material_info(self, parts: list[str]) -> None:
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

        # Basic check if the extracted term really is a material
        # Should be start with an upper case letter and not be in the dictionary of known galactic digits
        if material[0].islower() or material in self.galactic_digit_to_roman.keys():
            print(f'{material} does not seem to be a material. Input ignored.')
            return

        amount_galactic = parts[0:-4]
        amount_decimal = self.convert_galactic_to_decimal(amount_galactic)

        # amount_roman is None in case amount_galactic can not be converted to
        # a valid roman numeral and thus not to a decimal number.
        if amount_decimal is None:
            print('invalid input. Input ignored.')
        else:
            # Calculate and store the value of a single unit of the material.
            material_value = credits / amount_decimal
            self.material_values[material] = material_value

    def convert_galactic_to_decimal(self, galactic_digits: list[str]) -> Optional[int]:
        """
        Converts a list of galactic digits to a string containing the corresponding decimal number
        if the corresponding roman number is valid.
        :param galactic_digits: A list of galactic digits.
        :return: The corresponding decimal number. In case no valid roman numeral exists None is returned.
        """

        roman_numeral = []
        for galactic_digit in galactic_digits:

            # Information missing: If there is no known mapping from the galactic to a roman digit
            # ask the user to provide one.
            while galactic_digit not in self.galactic_digit_to_roman.keys():
                print(f'missing information / invalid input: How much is {galactic_digit} ?')

                # Expected input format is equal to the standard input, e.g.: glob is X
                user_in = input().strip().split(' ')

                if len(user_in) != 3: continue
                galactic_digit_new, _, roman_digit_new = user_in

                # Check if the galactic digit in the input matches the one requested and whether
                # a valid roman digit was provided.
                # In case the correct format was provided, store the information like in the non-missing case.
                if galactic_digit == galactic_digit_new and roman_digit_new in self.roman_digit_to_dec_value.keys():
                    self.galactic_digit_to_roman[galactic_digit] = roman_digit_new

            roman_digit = self.galactic_digit_to_roman.get(galactic_digit)
            roman_numeral.append(roman_digit)

        roman_numeral = "".join(roman_numeral)

        if self.is_valid_roman_numeral(roman_numeral):

            # A library function is used to convert the roman numeral into a decimal representation.
            decimal_number = roman.fromRoman(roman_numeral)
            return decimal_number
        else:
            return None

    def handle_request(self, parts: list[str]) -> None:

        if " ".join(parts[0:3]) == 'how much is':
            amount_galactic = parts[3:-1]
            amount_decimal = self.convert_galactic_to_decimal(amount_galactic)

            # None is returned in case amount_galactic can't be converted to a valid roman numeral
            # (and thus not into a decimal)
            if amount_decimal is None:
                print('invalid input. Input ignored.')
            else:
                print(f'{" ".join(amount_galactic)} is {amount_decimal}')
            return

        elif " ".join(parts[0:4]) == 'how many Credits is':

            # Covert the amount of material requested into the decimal representation
            amount_galactic = parts[4:-2]

            # No amount is given, e.g.: how many Credits is Iron ?
            if len(amount_galactic) == 0:
                amount_decimal = 1
                amount_galactic_output = ''
            else:
                amount_decimal = self.convert_galactic_to_decimal(amount_galactic)
                amount_galactic_output = " ".join(amount_galactic) + ' '

            # None is returned in case amount_galactic can't be converted to a valid roman numeral
            # (and thus not into a decimal)
            if amount_decimal is None:
                print('invalid input. Input ignored.')
                return

            # Get the material and its price per unit
            material = parts[-2]
            if material in self.material_values.keys():
                material_value = self.material_values.get(material)
            elif amount_galactic_output == '':
                # In case material and amount are missing.
                print('invalid input. Input ignored.')
                return
            else:
                print(f'unknown material: {material}')
                return

            overall_value = amount_decimal * material_value

            # Cast to integer to avoid decimal places in the output but only if the value does not have decimal places
            overall_value = int(overall_value) if overall_value.is_integer() else overall_value

            print(f'{amount_galactic_output}{material} is {overall_value} Credits')
            return

        else:
            # This answer is printed in case it is a request (input ending with a ?) that can't be interpreted at all.
            print('I have no idea what you are talking about')
            return

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

    @staticmethod
    def rule_compliant_subtraction(first_roman_digit: str, second_roman_digit: str) -> bool:
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

        if roman_numeral is None or roman_numeral == '':
            return False

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
                    if self.roman_digit_to_dec_value.get(prev_digit_2) < self.roman_digit_to_dec_value.get(
                            current_digit):
                        return False

        return True


if __name__ == '__main__':
    guc = GalacticUnitConverter()
    guc.convert()
