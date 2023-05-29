import subprocess
from colorama import Fore, Style


class PerformanceCheck:
    def __init__(self, compiler, ai, language):
        self.language = language
        self.code = ""
        self.generate_prompt = "Your task is to benchmark the input functions and compare their performance. Write a C++ application to measure the performance of two functions (original and improved codes); add 50 test cases with different complexities to consider various corner cases and give me a better estimation of the time complexity of both programs; run each test case 5 times. I give you the original code and the improved code, and I expect to have one main function that benchmarks both functions and returns one number in the output (no comment, only a single number) that reports the speedup of the improved code (dividing the average time of the improved code by the average time of the original code). Give me only the code and no explanation; save tokens. Say nothing else."
        self.fix_prompt = "The generated code is slower than the original. Please improve the following: "
        self.compiler = compiler
        self.ai = ai

    def generate_code(self, original_code, generated_code):
        prompt = self.generate_prompt + "\n\\original code\n"+original_code\
            + "\n\\improved code\n" + generated_code
        print(Fore.YELLOW + "Generating code..." + Style.RESET_ALL)
        self.code = self.ai.submit_task(prompt, self.code)
        self.code = self.compiler.check_and_fix(self.code, None, name='perf_code')

    def measure_performance(self, code):
        print(Fore.YELLOW + "Measuring performance..." + Style.RESET_ALL)
        process = subprocess.run(['./perf_code.out'], text=True, capture_output=True)

        if process.returncode != 0:  # Runtime error
            return None

        return process.stdout  # Speedup

    def measure_and_fix(self, input_code, generated_code):
        self.code = ''
        self.generate_code(input_code, generated_code)
        performance = self.measure_performance(self.code)
        if performance is None or performance < 1:  # Performance criteria not met
            print(Fore.RED + 'Performance criteria not met: ' + Style.RESET_ALL + performance)
            generated_code = self.ai.submit_task(self.fix_prompt, generated_code)
            self.verify_and_fix(input_code, generated_code)
