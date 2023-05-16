import input_handler
from ai_interface import AIInterface
from compilation_check import CompilationCheck
from verification import Verification
from performance_check import PerformanceCheck
import subprocess

def check_tools_installed(tools):
    for tool in tools:
        process = subprocess.run(['which', tool], text=True, capture_output=True)
        if process.returncode != 0:
            print(f"{tool} is not installed. Please install it before running this program.")
            return False
    return True

def main():

    if not check_tools_installed(['gcc', 'g++', 'clang', 'clang++', 'klee', 'ktest-tool']):
        return
    
    args = input_handler.parse_arguments()

    ai = AIInterface(args.ai)

    compiler = CompilationCheck(args.language, args.compiler)

    verifier = Verification(args.verification_type) if args.verify else None

    performance_checker = PerformanceCheck(args.language) if args.performance else None

    task_passed = False

    while not task_passed:
        generated_code = ai.submit_task(args.task, read_code(args.input))

        compilable, error = compiler.compile_code(generated_code)
        if not compilable:
            ai.submit_error(error)
            continue

        if args.verify:
            original_code = read_code(args.input)
            verification_passed, error = verifier.verify(original_code, generated_code)
            if not verification_passed:
                ai.submit_error(error)
                continue

        if args.performance:
            performance = performance_checker.measure_performance(generated_code)
            if performance is None or performance > 1.1:  # Performance criteria not met
                ai.submit_error('Performance criteria not met')
                continue

        task_passed = True

    print('Task passed all checks.')