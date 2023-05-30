import subprocess
from colorama import Fore, Style


class CompilationCheck:
    def __init__(self, ai, lagnuage, compiler):
        self.language = lagnuage
        self.compiler = compiler
        self.prompt = "If there is no main, add it and use this" \
            + "code/function. If there are compilation errors, fix all of them: "
        self.ai = ai
        self.count = 0

    def compile_code(self, code, name, SE=0):
        input_file = name+'.c' if self.language == 'C' else name+'.cpp'
        output_file = name+'.out' if SE == 0 else name+'.bc'
        se_compiler = 'clang' if self.language == 'C' else 'clang++'
        with open(input_file, 'w') as f:
            f.write(code)

        if SE == 1:
            compile_command = [se_compiler,
                               '-I', '/usr/local/include/klee/klee.h',
                               '-emit-llvm', '-c', '-g', '-O0', '-Xclang',
                               '-disable-O0-optnone', input_file,
                               '-o', output_file]
        else:
            compile_command = [self.compiler,
                               # '-Wall', '-Wextra', '-Werror',
                               input_file,
                               '-o', output_file]

        print(Fore.YELLOW + "Compiling code..." + Style.RESET_ALL)
        process = subprocess.run(compile_command, text=True,
                                 capture_output=True)

        if process.returncode != 0:  # Compilation error
            return False, process.stderr
        return True, None

    def check_and_fix(self, code, error, se=0, name='temp_code'):
        compilable, error = self.compile_code(code, name)
        if not compilable:
            print(Fore.RED + 'Compilation Error: ' + Style.RESET_ALL + error)
            self.count = self.count + 1
            print(Fore.YELLOW + "[" + str(self.count) + "] Attempting to fix compilation errors..."
                  + Style.RESET_ALL)
            code = self.ai.submit_task(self.prompt + error, code)
            return self.check_and_fix(code, error, name)
        self.count = 0
        return code
