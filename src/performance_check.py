import time

class PerformanceCheck:
    def __init__(self, language):
        self.language = language

    def measure_performance(self, code):
        with open('temp_code.c' if self.language == 'C' else 'temp_code.cpp', 'w') as f:
            f.write(code)

        if self.language == 'C':
            compile_command = ['gcc', 'temp_code.c', '-o', 'temp_code']
        else:  # C++
            compile_command = ['g++', 'temp_code.cpp', '-o', 'temp_code']

        process = subprocess.run(compile_command, text=True, capture_output=True)
        if process.returncode != 0:  # Compilation error
            return None

        start = time.perf_counter()
        process = subprocess.run(['./temp_code'], text=True, capture_output=True)
        end = time.perf_counter()

        if process.returncode != 0:  # Runtime error
            return None

        return end - start  # Execution time