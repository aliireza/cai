import input_handler
from ai_interface import AIInterface
from compilation_check import CompilationCheck
from verification import Verification
from performance_check import PerformanceCheck
import subprocess
import os
from colorama import Fore, Style


def check_tools_installed(tools):
    for tool in tools:
        process = subprocess.run(['which', tool], text=True,
                                 capture_output=True)
        if process.returncode != 0:
            print(Fore.RED +
                  f"{tool} is not installed. Please install it before running this program."
                  + Style.RESET_ALL)
            return False
    return True


def main():
    if not check_tools_installed(['gcc', 'g++', 'clang', 'clang++',
                                  'klee', 'ktest-tool']):
        return

    args = input_handler.parse_arguments()

    ai = AIInterface(args.ai)

    compiler = CompilationCheck(ai, args.language, args.compiler)

    verifier = Verification(compiler, ai)

    performance_checker = PerformanceCheck(compiler, ai, args.language) if args.performance else None

    input_code = input_handler.read_code(args.input)
    input_task = args.task
    print(Fore.CYAN + "Input code:\n" + Style.RESET_ALL + input_code)

    # Ensure the input code is compilable before performing any other tasks
    compiler.check_and_fix(input_code, None)
    print(Fore.GREEN + "Input code is compilable" + Style.RESET_ALL)
    input_filename = os.path.basename(args.input)
    temp_input = os.path.splitext(input_filename)[0] + "-compilable" \
        + os.path.splitext(input_filename)[1]
    with open(temp_input, 'w') as f:
        f.write(input_code)
    print("Output code is written to "+temp_input)

    generated_code = input_code
    current_task = input_task

    # Peform the main task
    print(Fore.CYAN + "Generating code for the input task: \n" + current_task + Style.RESET_ALL)
    generated_code = ai.submit_task(current_task, generated_code)
    if (generated_code == ""):
        return
    generated_code = compiler.check_and_fix(generated_code, None)
    print(generated_code)

    if args.verify:
        print(Fore.YELLOW + "Verifying code..." + Style.RESET_ALL)
        verifier.verify_and_fix(input_code, generated_code)

    if args.performance:
        print(Fore.YELLOW + "Checking performance..." + Style.RESET_ALL)
        performance_checker.measure_and_fix(input_code, generated_code)

    print(Fore.GREEN + 'Output code:\n' + generated_code + Style.RESET_ALL)
    with open(args.output, 'w') as f:
        f.write(generated_code)
    print("Output code is written to "+args.output)


if __name__ == "__main__":
    main()
