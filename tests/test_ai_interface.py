# python -m unittest test_ai_interface.py
import unittest
from unittest.mock import patch
import sys
import ai_interface
sys.path.insert(0, '../src/')


class TestAIInterface(unittest.TestCase):
    @patch('ai_interface.bardapi.core.Bard')
    @patch('ai_interface.AIInterface.bard_init', return_value=None)
    def test_init(self, MockInit, MockBard):
        # Test initialization with BARD
        ai = ai_interface.AIInterface('BARD')
        self.assertEqual(ai.ai_choice, 'BARD')
        MockInit.assert_called_once()

    @patch('ai_interface.bardapi.core.Bard')
    @patch('ai_interface.AIInterface.bard_init', return_value=None)
    def test_get_code_bard(self, MockInit, MockBard):
        ai = ai_interface.AIInterface('BARD')
        input = 'This is a test c++ Here is some code ```c++\nint a =1;```'
        expected = 'int a =1;'
        self.assertEqual(ai.get_code_bard(input), expected)

    @patch('ai_interface.bardapi.core.Bard')
    @patch('ai_interface.AIInterface.bard_init', return_value=None)
    def test_submit_task_bard(self, MockInit, MockBard):
        ai = ai_interface.AIInterface('BARD')
        ai.bard = MockBard()
        task = 'Your task is to fix any errors for a C++ function. I will provide you with a C++ function, and you should only return the full code (including the function and main()) to be able to test the function in the main and run it. no text, please; give me the code only. no extern C'
        code = '''int test(int x){
                    cout<< "Hello" endl
                    return 0
                }'''
        mock_response = {'content': 'Sure, here is the fixed code:\n\n```c++\n#include <iostream>\n\nint test(int x) {\n  std::cout << "Hello" << std::endl;\n  return 0;\n}\n\nint main() {\n  int x = 10;\n  test(x);\n  return 0;\n}\n```\n\nThis code will print the following to the console:\n\n```\nHello\n```'}

        # Configure the mock Bard object to return our mock_response
        MockBard.return_value.get_answer.return_value = mock_response

        expected = '''#include <iostream>

int test(int x) {
  std::cout << "Hello" << std::endl;
  return 0;
}

int main() {
  int x = 10;
  test(x);
  return 0;
}'''
        self.assertEqual(ai.submit_task_bard(task, code), expected)
        MockBard.return_value.get_answer.assert_called_once_with(task + "\n" + code)


if __name__ == '__main__':
    unittest.main()
