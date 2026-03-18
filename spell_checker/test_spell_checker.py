import unittest
from spell_checker import SpellChecker


class TestSpellChecker(unittest.TestCase):
    """
    Test suite for the SpellChecker implementation.

    These tests validate:
    - correctness of prefix-based suggestions
    - handling of empty and punctuation-only files
    - behaviour on small and unusual datasets
    - ranking behaviour across multiple custom test cases
    """

    def check_result(self, checker: SpellChecker, input_word: str, expected: list):
        """
        Helper function that checks:
        1. The returned suggestions match the expected suggestions
        2. No duplicate suggestions are returned
        """
        result = checker.check(input_word)
        error_message = f'Prompt "{input_word}" expected {expected} but got {result}'
        self.assertEqual(set(result), set(expected), error_message)
        self.assertEqual(len(result), len(expected), f'Duplicate element found in {result}')

    # Test 1: Validates behaviour on a file with nonsensical/random strings.
    # Ensures the spell checker can still return valid prefix-based suggestions,
    # even when the dataset contains unusual or long alphanumeric sequences.
    def test_nonsense_file(self):
        checker = SpellChecker('text_files/Nonsense.txt')
        self.check_result(checker, 'z', ['zzz'])
        self.check_result(
            checker,
            '0',
            ['0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefhijklmnopqrstuvz']
        )

    # Test 2: Validates behaviour when the input file is empty.
    # Ensures no suggestions are returned since no words exist in the Trie.
    def test_empty_file(self):
        checker = SpellChecker('text_files/Empty.txt')
        self.check_result(checker, 'z', [])

    # Test 3: Validates handling of punctuation-only input.
    # Ensures non-alphanumeric characters are ignored during preprocessing,
    # resulting in no valid words in the Trie.
    def test_punctuation_only_file(self):
        checker = SpellChecker('text_files/Punctuation.txt')
        self.check_result(checker, 'abc', [])

    # Test 4: Validates behaviour on a small dataset.
    # Ensures correct prefix matching and suggestion generation for short inputs.
    def test_small_file(self):
        checker = SpellChecker('text_files/Small.txt')
        self.check_result(checker, 'hh', ['h'])

    # Test 5: Validates behaviour for single-character datasets.
    # Ensures prefix matching works when only minimal data is available.
    def test_single_letter_file(self):
        checker = SpellChecker('text_files/A.txt')
        self.check_result(checker, 'aa', ['aaa'])

    # Test 6: Validates ranking and suggestion correctness on custom dataset 1.
    # Covers exact matches, partial matches, and ranking among multiple valid outputs.
    def test_case_1(self):
        checker = SpellChecker('text_files/test_case_1.txt')

        self.check_result(checker, 'IDc', ['IDA', 'IDC', 'IDJ'])
        self.check_result(checker, 'I', [])
        self.check_result(checker, 'Is', ['I', 'IDA', 'IDC'])
        self.check_result(checker, 'meow', ['me', 'm'])

    # Test 7: Validates ranking logic on custom dataset 2.
    # Ensures suggestions are correctly selected when multiple similar prefixes exist.
    def test_case_2(self):
        checker = SpellChecker('text_files/test_case_2.txt')

        self.check_result(checker, 'IDc', ['IDK', 'IDC', 'IDA'])
        self.check_result(checker, 'I', ['IDK', 'IDC', 'IDA'])
        self.check_result(checker, 'IDJM', ['IDJ', 'IDK', 'IDC'])
        self.check_result(checker, 'IDAB', ['IDA', 'IDAA', 'IDK'])

    # Test 8: Validates behaviour on a dataset with mixed words and varied prefixes.
    # Ensures case sensitivity and prefix matching operate correctly.
    def test_case_3(self):
        checker = SpellChecker('text_files/test_case_3.txt')

        self.check_result(checker, 'A', ['Aespa'])
        self.check_result(checker, 'W', ['Whiplash', 'Woncho'])
        self.check_result(checker, 'O', ['October21'])
        self.check_result(checker, 'Su', ['Supernova', 'Sageoneun'])
        self.check_result(checker, 'a', [])

    # Test 9: Validates behaviour where only a limited number of valid suggestions exist.
    def test_case_4(self):
        checker = SpellChecker('text_files/test_case_4.txt')
        self.check_result(checker, 'ID', ['IDAA', 'IDA'])

    # Test 10: Stress test using a very large dataset.
    # Ensures the implementation scales correctly and maintains performance
    # while still returning accurate top suggestions.
    def test_very_large_file(self):
        checker = SpellChecker('text_files/VeryLarge.txt')
        self.check_result(checker, 'Hello', ['Hel', 'Helsxa', 'HelynaR'])
        self.check_result(checker, 'l', [])
        self.check_result(checker, 'abc', ['abcI9E', 'abcZq0cY9sl18UB', 'ab'])
        self.check_result(checker, '2137', ['213', '213T', '213lTyc'])


if __name__ == '__main__':
    unittest.main()