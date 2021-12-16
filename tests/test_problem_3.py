import json

import pytest

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

    def test_adding_info_process_input_line(self):
        # Adding information via inputs

        self.guc.process_input_line('glob is I')
        self.guc.process_input_line('pish is X')
        self.guc.process_input_line('glob glob Silver is 34 Credits')
        assert self.guc.galactic_to_roman.get('glob') == 'I'
        assert self.guc.galactic_to_roman.get('pish') == 'X'
        assert self.guc.metal_values.get('Sliver') == 17

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

        # Get the last line printed
        def get_output_line():
            out, _ = capsys.readouterr()
            # -2 because the last entry is an empty string
            out = out.split('\n')[-2]
            return out

        # Requests via inputs
        self.guc.process_input_line("how much is pish tegj glob glob ?")
        assert get_output_line() == "pish tegj glob glob is 42"
        self.guc.process_input_line("how many Credits is glob prok Gold ?")
        assert get_output_line() == "glob prok Gold is 57800 Credits"

        # Re-setting values
        self.guc.process_input_line('glob is X')
        self.guc.process_input_line("how many Credits is glob glob Silver ?")
        assert self.guc.galactic_to_roman.get('glob') == 'X'
        assert get_output_line() == "glob glob Silver is 340 Credits"

        # TODO Add testes cases for missing information and other edge cases.
        # self.guc.process_input_line("how much wood could a woodchuck chuck if a woodchuck could chuck wood ?")
        # assert get_output_line() == "I have no idea what you are talking about"

    def test_general_sanity_check_roman_numerals(self):
        # The string should only contain valid roman numerals
        assert not self.guc.sanity_check_roman_numerals('a')

        # The string should not contain spaces or other control characters
        assert not self.guc.sanity_check_roman_numerals(' XI\n')

        # i is valid but should be upper case
        assert not self.guc.sanity_check_roman_numerals('i')

    def test_repetitions_sanity_check_roman_numerals(self):
        # Tests repetition of I, X, C and M, also subtraction to some degree for the separated by smaller value pattern
        assert self.guc.sanity_check_roman_numerals('X')
        assert self.guc.sanity_check_roman_numerals('XI')
        assert self.guc.sanity_check_roman_numerals('XIX')
        assert self.guc.sanity_check_roman_numerals('XXX')
        assert self.guc.sanity_check_roman_numerals('XXXI')
        assert self.guc.sanity_check_roman_numerals('XXXIX')

        # Subtracted numeral follows multiple times
        assert self.guc.sanity_check_roman_numerals('XIXII')
        assert self.guc.sanity_check_roman_numerals('XIXIII')

        # More complicated cases
        assert self.guc.sanity_check_roman_numerals('MDXIXI')
        assert self.guc.sanity_check_roman_numerals('MDXXIXI')
        assert self.guc.sanity_check_roman_numerals('MDXXXI')
        assert self.guc.sanity_check_roman_numerals('MMCDXXXIXIII')

        # More than 3 repetitions
        assert not self.guc.sanity_check_roman_numerals('MDXXXXI')

        # More than 3 / 4 repetitions is also caught in case of subtraction
        assert not self.guc.sanity_check_roman_numerals('XXXXIXX')
        assert not self.guc.sanity_check_roman_numerals('MDXXIXX')

        # D, L, V can never be repeated
        assert not self.guc.sanity_check_roman_numerals('DD')
        assert not self.guc.sanity_check_roman_numerals('DDXD')
        assert not self.guc.sanity_check_roman_numerals('MLL')

    def test_subtraction_sanity_check_roman_numerals(self):
        # "I" can be subtracted from "V" and "X" only.
        assert self.guc.sanity_check_roman_numerals('IV')
        assert self.guc.sanity_check_roman_numerals('IX')
        assert not self.guc.sanity_check_roman_numerals('IM')

        # "X" can be subtracted from "L" and "C" only.
        assert self.guc.sanity_check_roman_numerals('XL')
        assert self.guc.sanity_check_roman_numerals('XC')
        assert not self.guc.sanity_check_roman_numerals('XM')

        # "C" can be subtracted from "D" and "M" only.
        assert self.guc.sanity_check_roman_numerals('CD')
        assert self.guc.sanity_check_roman_numerals('CM')

        # "V", "L", and "D" can never be subtracted.
        assert not self.guc.sanity_check_roman_numerals('DM')
        assert not self.guc.sanity_check_roman_numerals('LC')
        assert not self.guc.sanity_check_roman_numerals('VX')

        # Only one small-value symbol may be subtracted from any large-value symbol.
        assert not self.guc.sanity_check_roman_numerals('IIX')
        assert not self.guc.sanity_check_roman_numerals('XXC')

        # Added later on
        assert not self.guc.sanity_check_roman_numerals('IXC')
        assert not self.guc.sanity_check_roman_numerals('MVIXC')
        assert not self.guc.sanity_check_roman_numerals('CIIX')
