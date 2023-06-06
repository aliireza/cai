import subprocess
from colorama import Fore, Style


# This class is used to compile code, check for errors and fix them using an AI interface
class CompilationCheck:
    def __init__(self, ai, lagnuage, compiler):
        self.language = lagnuage  # Programming language
        self.compiler = compiler  # Compiler to use
        self.prompt = "If there is no main, add it and use this" \
            + "code/function. If there are compilation errors, fix all of them: "
        self.ai = ai  # AI interface to use for fixing errors
        self.count = 0  # Number of attempts made to fix the code

    def compile_code(self, code, name, SE=0):
        # Generate filenames based on language
        input_file = name+'.c' if self.language == 'C' else name+'.cpp'
        output_file = name+'.out' if SE == 0 else name+'.bc'
        se_compiler = 'clang' if self.language == 'C' else 'clang++'

        # Write the code to a file
        with open(input_file, 'w') as f:
            f.write(code)

        # Compile the code
        if SE == 1:  # If special header is required
            compile_command = [se_compiler,
                               '-I', '/usr/local/include/klee/klee.h',
                               '-emit-llvm', '-c', '-g', '-O0', '-Xclang',
                               '-disable-O0-optnone', input_file,
                               '-o', output_file]
        else:  # If normal compiler is used
            compile_command = [self.compiler,
                               # '-Wall', '-Wextra', '-Werror',
                               input_file,
                               '-o', output_file]

        print(Fore.YELLOW + "Compiling code..." + Style.RESET_ALL)
        process = subprocess.run(compile_command, text=True,
                                 capture_output=True)

        if process.returncode != 0:  # If there's a compilation error
            return False, process.stderr
        return True, None

    def check_and_fix(self, code, error, se=0, name='temp_code'):
        # Try to compile the code and if it fails, use AI to fix it
        compilable, error = self.compile_code(code, name)
        if not compilable:
            print(Fore.RED + 'Compilation Error: ' + Style.RESET_ALL + error)
            self.count = self.count + 1
            print(Fore.YELLOW + "[" + str(self.count) + "] Attempting to fix compilation errors..."
                  + Style.RESET_ALL)
            code = self.ai.submit_task(self.prompt + error, code)  # Ask the AI to fix the error
            return self.check_and_fix(code, error, name)
        self.count = 0
        return code
