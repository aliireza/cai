# python -m unittest test_verification.py
import unittest
from unittest.mock import patch
import sys
import cai.verification


# class TestVerification(unittest.TestCase):
#     @patch('verification.run_KLEE')
#     def test_run_KLEE(self, mock_run_KLEE):
#         # assuming your function returns a list of test cases
#         mock_run_KLEE.return_value = ['test_case_1', 'test_case_2']
#         test_cases = verification.run_KLEE('input_code')
#         self.assertEqual(test_cases, ['test_case_1', 'test_case_2'])

#     # Add more test cases as needed


if __name__ == '__main__':
    unittest.main()
