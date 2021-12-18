import json
from io import StringIO

import pytest
import roman

from assignment.problem_3 import GalacticUnitConverter


@pytest.fixture(scope="session")
def loaded_test_data() -> dict:
    """
    Session wide fixture to loaded the input / output data once from a json file in the resource directory.
    :return: The test data as a dictionary
    """

    # Note: File paths should be outsourced to a configuration file in a production environment
    with open('../resources/io_test_data.json') as json_file:
        test_data = json.load(json_file)

    yield test_data


class TestGalacticUnitConverter:

    @pytest.fixture(autouse=True)
    def setup(self, loaded_test_data) -> None:
        """
        Prepares a new instance of the tested class for each test.
        :param loaded_test_data: The fixture which loaded the test data from a file such that it can be accessed from
        within the class without reloading it from disk each time.
        :return: None
        """

        self.guc = GalacticUnitConverter()
        self.io_test_sets: dict = loaded_test_data

    @pytest.fixture()
    def io_test_set(self, request) -> dict:
        """
        Returns a specific test subset from the test data, such that a parametrised test can be used to test all
        subsets.
        :param request: A request object with which @pytest.mark.parametrize passes a parameter.
        :return: A test data subset as dictionary with the name request.param.
        """

        yield self.io_test_sets.get(request.param)

    def test_general_is_valid_roman_numeral(self):
        # The string should only contain valid roman numerals
        assert not self.guc.is_valid_roman_numeral('a')

        # The string should not contain spaces or other control characters
        assert not self.guc.is_valid_roman_numeral(' XI\n')

        # i is valid but should be upper case
        assert not self.guc.is_valid_roman_numeral('i')

    def test_repetitions_is_valid_roman_numeral(self):
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

    def test_subtraction_is_valid_roman_numeral(self):
        # "I" can be subtracted from "V" and "X" only
        assert self.guc.is_valid_roman_numeral('IV')
        assert self.guc.is_valid_roman_numeral('IX')
        assert not self.guc.is_valid_roman_numeral('IM')

        # "X" can be subtracted from "L" and "C" only
        assert self.guc.is_valid_roman_numeral('XL')
        assert self.guc.is_valid_roman_numeral('XC')
        assert not self.guc.is_valid_roman_numeral('XM')

        # "C" can be subtracted from "D" and "M" only
        assert self.guc.is_valid_roman_numeral('CD')
        assert self.guc.is_valid_roman_numeral('CM')

        # "V", "L", and "D" can never be subtracted
        assert not self.guc.is_valid_roman_numeral('DM')
        assert not self.guc.is_valid_roman_numeral('LC')
        assert not self.guc.is_valid_roman_numeral('VX')

        # Only one small-value symbol may be subtracted from any large-value symbol
        assert not self.guc.is_valid_roman_numeral('IIX')
        assert not self.guc.is_valid_roman_numeral('XXC')

        # Added later on
        assert not self.guc.is_valid_roman_numeral('IXC')
        assert not self.guc.is_valid_roman_numeral('MVIXC')
        assert not self.guc.is_valid_roman_numeral('CIIX')

    def test_galactic_to_decimal_conversion(self):
        # Some default mapping from roman to galactic digits
        roman_to_galactic = {
            'I': 'GI',
            'V': 'GV',
            'X': 'GX',
            'L': 'GL',
            'C': 'GC',
            'D': 'GD',
            'M': 'GM'
        }

        # Simulate user input of this mapping
        for roman_rep, galactic_rep in roman_to_galactic.items():
            input_line = f'{galactic_rep} is {roman_rep}'
            self.guc.process_input_line(input_line)

        # For a list of numbers check if the conversion works as expected
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

        # This test is disabled because non integer valued materials are allowed (iron is )
        # Amount of credit not divisible by the amount ->  no integer material value
        # self.guc.process_input_line('mok Gold is 55 Credits')
        # assert self.get_output_line(capsys) == 'invalid input. Input ignored.'

        # Invalid roman number given as amount
        self.guc.process_input_line('pok pok mok Platin is 500 Credits')
        assert self.get_output_line(capsys) == 'invalid input. Input ignored.'
        self.guc.process_input_line('mok mok mok mok Platin is 500 Credits')
        assert self.get_output_line(capsys) == 'invalid input. Input ignored.'

        # No amount is given
        self.guc.process_input_line('pok Iron is 15 Credits')
        self.guc.process_input_line('how many Credits is Iron ?')
        assert self.get_output_line(capsys) == 'Iron is 15 Credits'

    @staticmethod
    def get_output_line(capsys) -> str:
        """
        Helper method to get the last line printed by the converter.
        :param capsys: A capsys fixture object.
        :return: The last line printed.
        """

        out, _ = capsys.readouterr()

        # -2 because the last entry is an empty string
        out = out.split('\n')[-2]

        return out

    def dynamic_input_test(self, monkeypatch, capsys, list_of_input_lines: list[str], ) -> list[str]:
        """
        Helper method to simulate input from the user and collect the output produced by the converter.
        :param monkeypatch: A monkeypatch fixture object.
        :param capsys: A capsys fixture object.
        :param list_of_input_lines: A list of lines that should simulate the user input.
        :return: The output printed by the converter as list of strings.
        """

        list_of_input_lines = list_of_input_lines.copy()

        # Necessary to terminate convert() without an error
        list_of_input_lines.append('\n')
        input_lines = StringIO('\n'.join(list_of_input_lines))
        monkeypatch.setattr('sys.stdin', input_lines)
        self.guc.convert()

        # Get output as single lines in a list, exclude the last one because this is always an empty string
        out = capsys.readouterr()[0].split('\n')[0:-1]
        return out

    def test_missing_info_process_input_line(self, monkeypatch, capsys):

        # Missing information in info about material
        user_inputs = [
            'pok is I', 'mok pok pok Iron is 24 Credits',
            # Expected output: 'missing information / invalid input: How much is mok ?',
            'mok is X',
        ]

        converter_output = self.dynamic_input_test(monkeypatch, capsys, user_inputs)
        assert converter_output[-1] == 'missing information / invalid input: How much is mok ?'

        # Missing information in request, including wrong answer
        user_inputs = [
            'how many Credits is zok Iron ?',
            # Expected output: 'missing information / invalid input: How much is zok ?'
            # User input is should be a roman digit
            'zok is 34',
            # Expected output: 'missing information / invalid input: How much is zok ?'
            'zok is L'
            # Expected output: 'zok Iron is 100 Credits'
        ]

        converter_output = self.dynamic_input_test(monkeypatch, capsys, user_inputs)
        assert converter_output[-3] == 'missing information / invalid input: How much is zok ?'
        assert converter_output[-2] == 'missing information / invalid input: How much is zok ?'
        assert converter_output[-1] == 'zok Iron is 100 Credits'

        # More than just one information is missing
        user_inputs = [
            'how much is rok plok ?',
            # Expected output: 'missing information / invalid input: How much is rok ?'
            'rok is L',
            # Expected output: 'missing information / invalid input: How much is plok ?'
            'plok is X',
            # Expected output: 'rok plok is 60'
        ]

        converter_output = self.dynamic_input_test(monkeypatch, capsys, user_inputs)
        assert converter_output[-3] == 'missing information / invalid input: How much is rok ?'
        assert converter_output[-2] == 'missing information / invalid input: How much is plok ?'
        assert converter_output[-1] == 'rok plok is 60'

    @pytest.mark.parametrize("io_test_set", ['predefined_test_set', 'alternative_test_set',
                                             'missing_info_test_set', 'error_test_set'], indirect=True)
    def test_convert(self, monkeypatch, capsys, io_test_set):

        # Type check fails because of @pytest.mark.parametrize-construcition
        # noinspection PyTypeChecker
        user_input, expected_output = io_test_set['user_input'], io_test_set['expected_output']

        # noinspection PyTypeChecker
        converter_output = self.dynamic_input_test(monkeypatch, capsys, user_input)

        # Check that every line in the output matches the excepted one
        assert len(converter_output) == len(expected_output)
        for converter_line, expected_line in zip(converter_output, expected_output):
            assert converter_line == expected_line

    def test_previous_bugs(self, capsys):

        # Correct handling of materials with non-integer values
        self.guc.process_input_line('glob is I')
        self.guc.process_input_line('prok is V')
        self.guc.process_input_line('pish is X')
        self.guc.process_input_line('pish pish Iron is 3910 Credits')
        self.guc.process_input_line('how many Credits is glob Iron ?')
        assert self.get_output_line(capsys) == 'glob Iron is 195.5 Credits'
        self.guc.process_input_line('how many Credits is glob prok Iron ?')
        assert self.get_output_line(capsys) == 'glob prok Iron is 782 Credits'

        # Missing coverage: material not given
        self.guc.process_input_line('lok is X')
        self.guc.process_input_line('how many Credits is lok ?')
        assert self.get_output_line(capsys) == 'invalid input. Input ignored.'
