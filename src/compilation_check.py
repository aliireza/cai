import subprocess

class CompilationCheck:
    def __init__(self,lagnuage, compiler):
        self.language = lagnuage
        self.compiler = compiler

    def compile_code(self, code):
        with open('temp_code.c' if self.language == 'C' else 'temp_code.cpp', 'w') as f:
            f.write(code)

        if self.language == 'C':
            compile_command = [ self.compiler, 'temp_code.c', '-o', 'temp_code']
        else:  # C++
            compile_command = [ self.compiler, 'temp_code.cpp', '-o', 'temp_code']

        process = subprocess.run(compile_command, text=True, capture_output=True)

        if process.returncode != 0:  # Compilation error
            return False, process.stderr
        return True, None