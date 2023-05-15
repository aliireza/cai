import subprocess

def check_tools_installed(tools):
    for tool in tools:
        process = subprocess.run(['which', tool], text=True, capture_output=True)
        if process.returncode != 0:
            print(f"{tool} is not installed. Please install it before running this program.")
            return False
    return True

def main():
    
    # Parse the command line arguments
    args = parse_arguments()

    # Check if the required tools are installed
    if args.compile and not check_tools_installed(['gcc', 'g++', 'clang', 'clang++']):
        return

    # Read the code from the input file
    with open(args.input, 'r') as f:
        original_code = f.read()

    # Create an AIInterface object and submit the task
    ai_interface = AIInterface(args.ai)
    generated_code = ai_interface.submit_task(args.task, original_code)

    # Perform a compilation check if the -c option is specified
    if args.compile:
        compiler = CompilationCheck(args.language)
        success, error = compiler.compile_code(generated_code)
        if not success:
            print(f"Compilation error: {error}")
            # Handle the error, e.g., resubmit the task to the AI
            return

    # Perform verification if the -v option is specified
    if args.verify:
        verifier = Verification('fuzzy')  # Or 'SE', depending on your requirements
        success, error = verifier.verify(original_code, generated_code)
        if not success:
            print(f"Verification error: {error}")
            # Handle the error, e.g., resubmit the task to the AI
            return

    # Perform a performance check if the -p option is specified
    if args.performance:
        performance_checker = PerformanceCheck(args.language)
        original_time = performance_checker.measure_performance(original_code)
        generated_time = performance_checker.measure_performance(generated_code)

        if original_time is None or generated_time is None:
            print("Performance check failed due to a runtime error.")
            return

        print(f"Original code execution time: {original_time} seconds")
        print(f"Generated code execution time: {generated_time} seconds")

if __name__ == '__main__':
    main()