import input_handler
from ai_interface import AIInterface
from compilation_check import CompilationCheck
from verification import Verification
from performance_check import PerformanceCheck
import subprocess
import os
from colorama import Fore, Back, Style

def check_tools_installed(tools):
    for tool in tools:
        process = subprocess.run(['which', tool], text=True, capture_output=True)
        if process.returncode != 0:
            print(Fore.RED + f"{tool} is not installed. Please install it before running this program." + Style.RESET_ALL)
            return False
    return True

def main():

    if not check_tools_installed(['gcc', 'g++', 'clang', 'clang++', 'klee', 'ktest-tool']):
        return
    
    args = input_handler.parse_arguments()

    ai = AIInterface(args.ai)

    compiler = CompilationCheck(args.language, args.compiler)

    verifier = Verification()

    performance_checker = PerformanceCheck(args.language) if args.performance else None

    task_passed = False

    input_code = input_handler.read_code(args.input)
    input_task = args.task
    compile_task = "If there is no main, add it and use this code/functioin. If there are compilation errors, fix all of them: "
    verifier_task = "I got these errors from KLEE. Please fix all of them: "
    print(Fore.CYAN + "Input code:\n" + Style.RESET_ALL + input_code)
    

    # Ensure the input code is compilable before performing any other tasks
    input_compilable = False
    count = 0
    while not input_compilable:
        compilable, error = compiler.compile_code(input_code)
        if not compilable:
            print(Fore.RED + 'Compilation Error: ' + Style.RESET_ALL + error)
            count = count + 1
            print(Fore.YELLOW + '[' + str(count) + '] Attempting to fix compilation errors...' + Style.RESET_ALL)
            input_code = ai.submit_task(compile_task + error, input_code)
            continue
        count = 0
        input_compilable = True

    print(Fore.GREEN + "Input code is compilable" + Style.RESET_ALL)
    input_filename = os.path.basename(args.input)
    temp_input = os.path.splitext(input_filename)[0]+ "-compilable" + os.path.splitext(input_filename)[1]
    with open(temp_input, 'w') as f:
        f.write(input_code)
    print("Output code is written to "+temp_input)

    generated_code = input_code
    current_task = input_task

    # Peform the main task
    while not task_passed:
        print(Fore.CYAN + "Generating code for the input task: \n" + current_task + Style.RESET_ALL )
        generated_code = ai.submit_task(current_task, generated_code)
        if(generated_code == ""):
            return

        print(generated_code)

        compilable, error = compiler.compile_code(generated_code)
        if(error is not None):
            print(error)
        if not compilable:
            generated_code = ai.submit_task(compile_task + error, generated_code)
            continue

        if args.verify:
            print(Fore.YELLOW + "Verifying code..." + Style.RESET_ALL)
            verification_passed, error = verifier.verify(compiler, ai, input_code, generated_code)
            if not verification_passed:
                print(Fore.RED + 'Verification Error: ' + Style.RESET_ALL + error)
                generated_code = ai.submit_task(verifier_task + error, generated_code)
                continue

        if args.performance:
            print(Fore.YELLOW + "Checking performance..." + Style.RESET_ALL)
            if(performance_checker.code == ''):
                performance_checker.generate_code(compiler,ai,input_code,generated_code)
            print(performance_checker.code)
            performance = performance_checker.measure_performance(generated_code)
            if performance is None or performance < 1:  # Performance criteria not met
                print('Performance criteria not met')
                current_task = current_task + "performance criteria not met; improve again"
                continue

        task_passed = True

        print(Fore.GREEN + 'Task passed all checks.\n\nOutput code:\n' + generated_code + Style.RESET_ALL)
        with open(args.output, 'w') as f:
            f.write(generated_code)
        print("Output code is written to "+args.output)

if __name__ == "__main__":
    main()
