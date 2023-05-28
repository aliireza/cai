import time
import subprocess

class PerformanceCheck:
    def __init__(self, language):
        self.language = language
        self.code = ""
        self.prompt = "Your task is to benchmark the input functions and compare their performance. Write a C++ application to measure the performance of two functions (original and improved codes); add 50 test cases with different complexities to consider various corner cases and give me a better estimation of the time complexity of both programs; run each test case 5 times. I give you the original code and the improved code, and I expect to have one main function that benchmarks both functions and returns one number in the output (no comment, only a single number) that reports the speedup of the improved code (dividing the average time of the improved code by the average time of the original code). Give me only the code and no explanation; save tokens. Say nothing else."

    def generate_code(self, compiler, ai, original_code, generated_code):
        input_compilable = False
        self.prompt = self.prompt + "\n\\original code\n"+original_code + "\n\\improved code\n" + generated_code
        print(Fore.YELLOW + "Generating code..." + Style.RESET_ALL)
        self.code = ai.submit_task( self.prompt, self.code)
        compile_task = "If there is not main; add it and use this code. If there is compilation erros, fix all of them: "
        
        while not input_compilable:
            compilable, error = compiler.compile_code(self.code, name='perf_code')
            print((error))
            if not compilable:
                self.code = ai.submit_task(compile_task + error, self.code)
                continue
            input_compilable = True


    def measure_performance(self, code):
        print(Fore.YELLOW + "Measuring performance..." + Style.RESET_ALL)
        process = subprocess.run(['./perf_code.out'], text=True, capture_output=True)

        if process.returncode != 0:  # Runtime error
            return None

        return process.stdout # Speedup