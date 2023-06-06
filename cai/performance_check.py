import subprocess
from colorama import Fore, Style


# This class is used to measure and compare the performance of two pieces of code.
class PerformanceCheck:
    def __init__(self, compiler, ai, language):
        self.language = language  # Programming language
        self.code = ""  # The code to be tested
        # This prompt is used to generate a benchmarking application that measures and compares the performance of the original code and the generated code.
        self.generate_prompt = "Your task is to benchmark the input functions and compare their performance. Write a C++ application to measure the performance of two functions (original and improved codes); add 50 test cases with different complexities to consider various corner cases and give me a better estimation of the time complexity of both programs; run each test case 5 times. I give you the original code and the improved code, and I expect to have one main function that benchmarks both functions and returns one number in the output (no comment, only a single number) that reports the speedup of the improved code (dividing the average time of the improved code by the average time of the original code). Give me only the code and no explanation; save tokens. Say nothing else."
        # This prompt is used to improve the generated code if it is slower than the original code.
        self.fix_prompt = "The generated code is slower than the original. Please improve the following: "
        self.compiler = compiler  # The compiler to use
        self.ai = ai  # The AI interface to use for generating and fixing the code

    def generate_code(self, original_code, generated_code):
        # Generate a benchmarking application using the AI interface
        prompt = self.generate_prompt + "\n\\original code\n"+original_code\
            + "\n\\improved code\n" + generated_code
        print(Fore.YELLOW + "Generating code..." + Style.RESET_ALL)
        self.code = self.ai.submit_task(prompt, self.code)
        self.code = self.compiler.check_and_fix(self.code, None, name='perf_code')

    def measure_performance(self, code):
        # Measure the performance of the code
        print(Fore.YELLOW + "Measuring performance..." + Style.RESET_ALL)
        process = subprocess.run(['./perf_code.out'], text=True, capture_output=True)

        if process.returncode != 0:  # If there's a runtime error
            return None

        return process.stdout  # Return the performance measurement (speedup)

    def measure_and_fix(self, input_code, generated_code):
        # Measure the performance of the code and if it does not meet the performance criteria, use AI to fix it
        self.code = ''
        self.generate_code(input_code, generated_code)
        performance = self.measure_performance(self.code)
        if performance is None or performance < 1:  # If the performance criteria are not met
            print(Fore.RED + 'Performance criteria not met: ' + Style.RESET_ALL + performance)
            generated_code = self.ai.submit_task(self.fix_prompt, generated_code)  # Ask the AI to fix the code
            self.verify_and_fix(input_code, generated_code)
