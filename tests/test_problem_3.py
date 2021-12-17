import json

import pytest
import roman

from assignment.problem_3 import GalacticUnitConverter


@pytest.fixture(scope="session")
def loaded_test_data():
    """
    Session wide fixture to loaded the input / output data once from a json file in the resource directory.
    :return:
    """
    with open('../resources/io_test_data.json') as json_file:
        test_data = json.load(json_file)

    yield test_data


class TestGalacticUnitConverter:

    @pytest.fixture(autouse=True)
    def setup(self, loaded_test_data):
        self.guc = GalacticUnitConverter()
        self.io_test_sets: dict = loaded_test_data

    @pytest.fixture()
    def io_test_set(self, request):
        yield self.io_test_sets.get(request.param)

    # TODO Enable again
    # TODO Add additional test sets: 'alternative_test_set', 'missing_info_test_set', 'error_test_set'
    # @pytest.mark.parametrize("io_test_set", ['predefined_test_set'], indirect=True)
    # def test_convert(self, io_test_set):
    #    user_input, expected_output = io_test_set

    def test_galactic_to_decimal_conversion(self):
        roman_to_galactic = {
            'I': 'GI',
            'V': 'GV',
            'X': 'GX',
            'L': 'GL',
            'C': 'GC',
            'D': 'GD',
            'M': 'GM'
        }

        for roman_rep, galactic_rep in roman_to_galactic.items():
            input_line = f'{galactic_rep} is {roman_rep}'
            self.guc.process_input_line(input_line)

        tested_numbers = [1, 10, 77, 250, 999, 1000, 2523]

        for number in tested_numbers:
            roman_rep = roman.toRoman(number)
            galactic_rep = [roman_to_galactic.get(digit) for digit in roman_rep]
            assert self.guc.convert_galactic_to_decimal(galactic_rep) == number

    def test_adding_info_process_input_line(self):
        # Add information via inputs lines
        self.guc.process_input_line('glob is I')
        self.guc.process_input_line('pish is X')
        self.guc.process_input_line('glob glob Silver is 34 Credits')

        # Checks if the information was extracted and stored correctly
        assert self.guc.galactic_digit_to_roman.get('glob') == 'I'
        assert self.guc.galactic_digit_to_roman.get('pish') == 'X'
        assert self.guc.material_values.get('Silver') == 17

    # Get the last line printed
    def get_output_line(self, capsys):
        out, _ = capsys.readouterr()
        # -2 because the last entry is an empty string
        out = out.split('\n')[-2]
        return out

    def test_requests_process_input_line(self, capsys):
        user_info_input = [
            "glob is I",
            "prok is V",
            "pish is X",
            "tegj is L",
            "glob glob Silver is 34 Credits",
            "glob prok Gold is 57800 Credits",
            "pish pish Iron is 3910 Credits",
        ]

        for line in user_info_input:
            self.guc.process_input_line(line)

        # Requests via inputs
        self.guc.process_input_line("how much is pish tegj glob glob ?")
        assert self.get_output_line(capsys) == "pish tegj glob glob is 42"
        self.guc.process_input_line("how many Credits is glob prok Silver ?")
        assert self.get_output_line(capsys) == "glob prok Silver is 68 Credits"
        self.guc.process_input_line("how many Credits is glob prok Gold ?")
        assert self.get_output_line(capsys) == "glob prok Gold is 57800 Credits"

        # Re-setting values
        self.guc.process_input_line('glob is X')
        self.guc.process_input_line("how many Credits is glob glob Silver ?")
        assert self.guc.galactic_digit_to_roman.get('glob') == 'X'
        assert self.get_output_line(capsys) == "glob glob Silver is 340 Credits"

    def test_exceptional_inputs_process_input_line(self, capsys):

        # General inputs that can't be interpreted meaningfully
        self.guc.process_input_line('')
        assert self.get_output_line(capsys) == 'invalid input. Input ignored.'

        self.guc.process_input_line('invalid input')
        assert self.get_output_line(capsys) == 'invalid input. Input ignored.'

        self.guc.process_input_line('I is pok')
        assert self.get_output_line(capsys) == 'invalid input. Input ignored.'

        # Requests that can't be answered
        self.guc.process_input_line('how many Credits is ?')
        assert self.get_output_line(capsys) == 'invalid input. Input ignored.'

        self.guc.process_input_line('how much wood could a woodchuck chuck if a woodchuck could chuck wood ?')
        assert self.get_output_line(capsys) == "I have no idea what you are talking about"

        self.guc.process_input_line('what time is it ?')
        assert self.get_output_line(capsys) == "I have no idea what you are talking about"

        self.guc.process_input_line('how many Credits do pok Iron cost ?')
        assert self.get_output_line(capsys) == "I have no idea what you are talking about"

        # Invalid roman digits used when defining
        self.guc.process_input_line('pok is K')
        assert self.get_output_line(capsys) == 'invalid input. Input ignored.'
        self.guc.process_input_line('pok is XI')
        assert self.get_output_line(capsys) == 'invalid input. Input ignored.'
        self.guc.process_input_line('pok is x')
        assert self.get_output_line(capsys) == 'invalid input. Input ignored.'

        # Wrong unit given
        self.guc.process_input_line('pok is I')
        self.guc.process_input_line('pok pok Gold is 300 Dollar')
        assert self.get_output_line(capsys) == 'invalid input. Input ignored.'

        self.guc.process_input_line('pok is I')
        self.guc.process_input_line('zok is V')
        self.guc.process_input_line('mok is X')

        # No material given when adding information
        self.guc.process_input_line('mok pok is 100 Credits')
        assert self.get_output_line(capsys) == 'pok does not seem to be a material. Input ignored.'

        # Unknown material given in a request
        self.guc.process_input_line('how many Credits is pok pok Copper ?')
        assert self.get_output_line(capsys) == 'unknown material: Copper'

        # Amount of credit not divisible by the amount ->  no integer material value
        self.guc.process_input_line('mok Gold is 55 Credits')
        assert self.get_output_line(capsys) == 'invalid input. Input ignored.'

        # Invalid roman number given as amount
        self.guc.process_input_line('pok pok mok Platin is 500 Credits')
        assert self.get_output_line(capsys) == 'invalid input. Input ignored.'
        self.guc.process_input_line('mok mok mok mok Platin is 500 Credits')
        assert self.get_output_line(capsys) == 'invalid input. Input ignored.'

    def test_general_sanity_check_roman_numerals(self):
        # The string should only contain valid roman numerals
        assert not self.guc.is_valid_roman_numeral('a')

        # The string should not contain spaces or other control characters
        assert not self.guc.is_valid_roman_numeral(' XI\n')

        # i is valid but should be upper case
        assert not self.guc.is_valid_roman_numeral('i')

    def test_repetitions_sanity_check_roman_numerals(self):
        # Tests repetition of I, X, C and M, also subtraction to some degree for the separated by smaller value pattern
        assert self.guc.is_valid_roman_numeral('X')
        assert self.guc.is_valid_roman_numeral('XI')
        assert self.guc.is_valid_roman_numeral('XIX')
        assert self.guc.is_valid_roman_numeral('XXX')
        assert self.guc.is_valid_roman_numeral('XXXI')
        assert self.guc.is_valid_roman_numeral('XXXIX')

        # Subtracted numeral follows multiple times
        assert self.guc.is_valid_roman_numeral('XIXII')
        assert self.guc.is_valid_roman_numeral('XIXIII')

        # More complicated cases
        assert self.guc.is_valid_roman_numeral('MDXIXI')
        assert self.guc.is_valid_roman_numeral('MDXXIXI')
        assert self.guc.is_valid_roman_numeral('MDXXXI')
        assert self.guc.is_valid_roman_numeral('MMCDXXXIXIII')

        # More than 3 repetitions
        assert not self.guc.is_valid_roman_numeral('MDXXXXI')

        # More than 3 / 4 repetitions is also caught in case of subtraction
        assert not self.guc.is_valid_roman_numeral('XXXXIXX')
        assert not self.guc.is_valid_roman_numeral('MDXXIXX')

        # D, L, V can never be repeated
        assert not self.guc.is_valid_roman_numeral('DD')
        assert not self.guc.is_valid_roman_numeral('DDXD')
        assert not self.guc.is_valid_roman_numeral('MLL')

    def test_subtraction_sanity_check_roman_numerals(self):
        # "I" can be subtracted from "V" and "X" only.
        assert self.guc.is_valid_roman_numeral('IV')
        assert self.guc.is_valid_roman_numeral('IX')
        assert not self.guc.is_valid_roman_numeral('IM')

        # "X" can be subtracted from "L" and "C" only.
        assert self.guc.is_valid_roman_numeral('XL')
        assert self.guc.is_valid_roman_numeral('XC')
        assert not self.guc.is_valid_roman_numeral('XM')

        # "C" can be subtracted from "D" and "M" only.
        assert self.guc.is_valid_roman_numeral('CD')
        assert self.guc.is_valid_roman_numeral('CM')

        # "V", "L", and "D" can never be subtracted.
        assert not self.guc.is_valid_roman_numeral('DM')
        assert not self.guc.is_valid_roman_numeral('LC')
        assert not self.guc.is_valid_roman_numeral('VX')

        # Only one small-value symbol may be subtracted from any large-value symbol.
        assert not self.guc.is_valid_roman_numeral('IIX')
        assert not self.guc.is_valid_roman_numeral('XXC')

        # Added later on
        assert not self.guc.is_valid_roman_numeral('IXC')
        assert not self.guc.is_valid_roman_numeral('MVIXC')
        assert not self.guc.is_valid_roman_numeral('CIIX')
