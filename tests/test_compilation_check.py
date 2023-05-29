# python -m unittest test_compilation_check.py
import unittest
import sys
sys.path.insert(0, '../src/')
from compilation_check import CompilationCheck


class TestCompilationCheck(unittest.TestCase):
    def test_compile_code_c_gcc(self):
        compiler = CompilationCheck('C', 'gcc')

        # Test a compilable C code
        code = """
        #include <stdio.h>

        int main() {
            printf("Hello, World!");
            return 0;
        }
        """
        success, error = compiler.compile_code(code)
        self.assertTrue(success)
        self.assertIsNone(error)

        # Test a non-compilable C code
        code = """
        #include <stdio.h>

        int main() {
            printf("Hello, World!")
            return 0;
        }
        """  # Missing semicolon
        success, error = compiler.compile_code(code)
        self.assertFalse(success)
        self.assertIsNotNone(error)

    def test_compile_code_cpp_gcc(self):
        compiler = CompilationCheck('C++', 'g++')

        # Test a compilable C++ code
        code = """
        #include <iostream>

        int main() {
            std::cout << "Hello, World!";
            return 0;
        }
        """
        success, error = compiler.compile_code(code)
        self.assertTrue(success)
        self.assertIsNone(error)

        # Test a non-compilable C++ code
        code = """
        #include <iostream>

        int main() {
            std::cout << "Hello, World!"
            return 0;
        }
        """  # Missing semicolon
        success, error = compiler.compile_code(code)
        self.assertFalse(success)
        self.assertIsNotNone(error)

    def test_compile_code_c_clang(self):
        compiler = CompilationCheck('C', 'clang')

        # Test a compilable C code
        code = """
        #include <stdio.h>

        int main() {
            printf("Hello, World!");
            return 0;
        }
        """
        success, error = compiler.compile_code(code)
        self.assertTrue(success)
        self.assertIsNone(error)

        # Test a non-compilable C code
        code = """
        #include <stdio.h>

        int main() {
            printf("Hello, World!")
            return 0;
        }
        """  # Missing semicolon
        success, error = compiler.compile_code(code)
        self.assertFalse(success)
        self.assertIsNotNone(error)

    def test_compile_code_cpp_clang(self):
        compiler = CompilationCheck('C++', 'clang++')

        # Test a compilable C++ code
        code = """
        #include <iostream>

        int main() {
            std::cout << "Hello, World!";
            return 0;
        }
        """
        success, error = compiler.compile_code(code)
        self.assertTrue(success)
        self.assertIsNone(error)

        # Test a non-compilable C++ code
        code = """
        #include <iostream>

        int main() {
            std::cout << "Hello, World!"
            return 0;
        }
        """  # Missing semicolon
        success, error = compiler.compile_code(code)
        self.assertFalse(success)
        self.assertIsNotNone(error)


if __name__ == '__main__':
    unittest.main()
