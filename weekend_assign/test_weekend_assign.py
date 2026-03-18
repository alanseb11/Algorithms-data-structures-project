import unittest
from weekend_assign import assign


class TestAssign(unittest.TestCase):
    """
    Test suite for the weekend activity assignment problem.

    These tests validate:
    - correct assignment of participants to activities
    - handling of invalid scenarios (returning None)
    - adherence to capacity constraints
    - ensuring all participants are assigned exactly once
    """

    # Helper function: checks if the result matches the expected grouping
    # Ignores ordering within each activity (since multiple valid solutions may exist)
    def check_ans(self, preferences, places, expected):
        result = assign(preferences, places)
        error_message = f'Expected {expected} but got {result}'
        if len(expected) != len(result):
            return error_message
        for i in range(len(expected)):
            if set(expected[i]) != set(result[i]):
                return error_message
        return None

    # Helper function: ensures the function correctly returns None for invalid inputs
    def expected_none(self, preferences, places):
        result = assign(preferences, places)
        error_message = f'Expected None but got {result}'
        self.assertIsNone(result, error_message)

    # Test 1: Invalid cases where no valid assignment exists.
    # Ensures the function correctly returns None when constraints cannot be satisfied.
    def test_none_examples(self):
        preferences = [[2, 2], [1, 1], [0, 1], [2, 2], [1, 2]]
        places = [3, 2]
        self.expected_none(preferences, places)

        preferences = [[2, 0], [2, 0], [2, 0], [2, 0], [2, 0]]
        places = [3, 2]
        self.expected_none(preferences, places)

        preferences = [[0, 2], [0, 2], [0, 2], [0, 2], [0, 2]]
        places = [3, 2]
        self.expected_none(preferences, places)

        preferences = [[1, 2], [1, 2], [1, 2], [1, 2], [1, 2]]
        places = [3, 2]
        self.expected_none(preferences, places)

        preferences = [[2, 1], [2, 1], [2, 1], [2, 1], [2, 1]]
        places = [3, 2]
        self.expected_none(preferences, places)

        preferences = [[2, 2], [1, 1], [1, 1], [2, 2], [1, 1]]
        places = [3, 2]
        self.expected_none(preferences, places)

        preferences = [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1]]
        places = [3, 2]
        self.expected_none(preferences, places)

    # Test 2: Valid assignment scenarios.
    # Ensures participants are correctly grouped into activities based on preferences and constraints.
    def test_other_examples(self):

        # Case 1: Standard valid allocation with fixed expected grouping
        preferences = [[2, 1], [2, 1], [2, 0], [1, 2], [1, 2]]
        places = [3, 2]
        expected = [[0, 1, 2], [3, 4]]
        msg = self.check_ans(preferences, places, expected)
        self.assertIsNone(msg, msg)

        # Case 2: Multiple valid solutions possible
        # Ensures algorithm can return any valid grouping
        preferences = [[2, 1], [2, 1], [2, 0], [1, 2], [1, 2]]
        places = [2, 3]
        expected = [
            [[1, 2], [0, 3, 4]],
            [[0, 2], [1, 3, 4]]
        ]
        for lst in expected:
            msg = self.check_ans(preferences, places, lst)
            if msg is None:
                break
        self.assertIsNone(msg, msg)

        # Case 3: All participants willing for all activities
        # Ensures capacity constraints are respected
        preferences = [[2, 2], [2, 2], [2, 2], [2, 2], [2, 2]]
        places = [2, 3]
        result = assign(preferences, places)

        self.assertEqual(len(result), 2)
        self.assertEqual(len(result[0]), 2)
        self.assertEqual(len(result[1]), 3)

        all_activities = set(result[0]) | set(result[1])
        self.assertEqual(len(all_activities), 5)

        # Case 4: Same participants, different capacity distribution
        preferences = [[2, 2], [2, 2], [2, 2], [2, 2], [2, 2]]
        places = [3, 2]
        result = assign(preferences, places)

        self.assertEqual(len(result), 2)
        self.assertEqual(len(result[0]), 3)
        self.assertEqual(len(result[1]), 2)

        all_activities = set(result[0]) | set(result[1])
        self.assertEqual(len(all_activities), 5)

        # Case 5: Larger input with more activities
        # Ensures scalability and correct distribution across multiple groups
        preferences = [[2, 2, 2]] * 8
        places = [3, 3, 2]
        result = assign(preferences, places)

        self.assertEqual(len(result), 3)
        self.assertEqual(len(result[0]), 3)
        self.assertEqual(len(result[1]), 3)
        self.assertEqual(len(result[2]), 2)

        all_activities = set(result[0]) | set(result[1]) | set(result[2])
        self.assertEqual(len(all_activities), 8)


if __name__ == '__main__':
    unittest.main()