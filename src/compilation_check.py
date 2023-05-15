import subprocess

class CompilationCheck:
    def __init__(self, language):
        self.language = language

    def compile_code(self, code):
        with open('temp_code.c' if self.language == 'C' else 'temp_code.cpp', 'w') as f:
            f.write(code)

        if self.language == 'C':
            compile_command = ['gcc', 'temp_code.c', '-o', 'temp_code']
        else:  # C++
            compile_command = ['g++', 'temp_code.cpp', '-o', 'temp_code']

        process = subprocess.run(compile_command, text=True, capture_output=True)

        if process.returncode != 0:  # Compilation error
            return False, process.stderr
        return True, None