#!/usr/bin/env python3
"""
CAI Program
"""
from cai.input_handler import *
from cai.ai_interface import AIBuilder
from cai.compilation_check import CompilationCheck
from cai.verification import Verification
from cai.performance_check import PerformanceCheck
import subprocess
import os
from colorama import Fore, Style


# Function to check if necessary tools are installed
def check_tools_installed(tools):
    for tool in tools:
        process = subprocess.run(['which', tool], text=True,
                                 capture_output=True)
        # If tool is not found, print error and return False
        if process.returncode != 0:
            print(Fore.RED +
                  f"{tool} is not installed. Please install it before running this program."
                  + Style.RESET_ALL)
            return False
    return True


# Main function
def main():
    # Check if required tools are installed
    if not check_tools_installed(['gcc', 'g++', 'clang', 'clang++',
                                  'klee', 'ktest-tool']):
        return

    # Parse arguments
    args = parse_arguments()

    # Initialize AI interface, compilation checker, verifier and performance checker
    ai = AIBuilder(args.ai)
    compiler = CompilationCheck(ai, args.language, args.compiler)
    verifier = Verification(compiler, ai)
    performance_checker = PerformanceCheck(compiler, ai, args.language) if args.performance else None

    # Read input code and print it
    input_code = read_code(args.input)
    input_task = args.task
    print(Fore.CYAN + "Input code:\n" + Style.RESET_ALL + input_code)

    # Ensure the input code is compilable before performing any other tasks
    input_code = compiler.check_and_fix(input_code, None)
    print(Fore.GREEN + "Input code is compilable" + Style.RESET_ALL)
    print(input_code)

    # Write input code to temporary file
    input_filename = os.path.basename(args.input)
    temp_input = os.path.splitext(input_filename)[0] + "-compilable" \
        + os.path.splitext(input_filename)[1]
    with open(temp_input, 'w') as f:
        f.write(input_code)
    print("Output code is written to "+temp_input)

    # Initialize generated code and current task
    generated_code = input_code
    current_task = input_task

    # Perform the input task
    print(Fore.CYAN + "Generating code for the input task: \n" + current_task + Style.RESET_ALL)
    # Generate code and check if it is compilable
    generated_code = ai.submit_task(current_task, generated_code)
    if (generated_code == ""):
        return
    generated_code = compiler.check_and_fix(generated_code, None)
    print(generated_code)

    # If verify flag is set, verify the generated code
    if args.verify:
        print(Fore.YELLOW + "Verifying code..." + Style.RESET_ALL)
        verifier.verify_and_fix(input_code, generated_code)

    # If performance flag is set, measure the performance
    if args.performance:
        print(Fore.YELLOW + "Checking performance..." + Style.RESET_ALL)
        performance_checker.measure_and_fix(input_code, generated_code)

    # Print the generated code and write it to output file
    print(Fore.GREEN + 'Output code:\n' + generated_code + Style.RESET_ALL)
    with open(args.output, 'w') as f:
        f.write(generated_code)
    print("Output code is written to "+args.output)


# Run main function if the script is executed directly
if __name__ == "__main__":
    main()
