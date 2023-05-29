# python -m unittest test_input_handler.py
import unittest
from unittest.mock import patch
import sys
import argparse
sys.path.insert(0, '../src/')
import input_handler


class TestInputHandler(unittest.TestCase):
    @patch('argparse.ArgumentParser.parse_args')
    def test_parse_arguments(self, mock_parse_args):
        # Test case for C language, compilation check enabled, gcc as compiler
        mock_parse_args.return_value = argparse.Namespace(language='C',
                                                          compile=True,
                                                          compiler='gcc',
                                                          verify=False,
                                                          performance=False,
                                                          ai='OpenAI',
                                                          task='task1',
                                                          input='input.c')
        args = input_handler.parse_arguments()
        self.assertEqual(args.language, 'C')
        self.assertEqual(args.compile, True)
        self.assertEqual(args.compiler, 'gcc')
        self.assertEqual(args.verify, False)
        self.assertEqual(args.performance, False)
        self.assertEqual(args.ai, 'OpenAI')
        self.assertEqual(args.task, 'task1')
        self.assertEqual(args.input, 'input.c')

        # Add more test cases as needed


if __name__ == '__main__':
    unittest.main()
