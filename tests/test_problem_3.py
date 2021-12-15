from assignment.problem_3 import GalacticUnitConverter


class TestGalacticUnitConverter:

    def setup(self):
        self.guc = GalacticUnitConverter()

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
