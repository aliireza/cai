import subprocess

class CompilationCheck:
    def __init__(self,lagnuage, compiler):
        self.language = lagnuage
        self.compiler = compiler

    def compile_code(self, code, SE=0, name='temp_code'):
        input_file = name+'.c' if self.language == 'C' else name+'.cpp'
        output_file = name if SE == 0 else name+'.bc'
        se_compiler = 'clang' if self.language == 'C' else 'clang++'
        with open(input_file, 'w') as f:
            f.write(code)

        if SE == 1:
            compile_command = [ se_compiler, '-I', '/usr/local/include/klee/klee.h', '-emit-llvm', '-c', '-g', '-O0', '-Xclang', '-disable-O0-optnone', input_file, '-o', output_file]
        else:
                compile_command = [ self.compiler, input_file, '-o', output_file]

        process = subprocess.run(compile_command, text=True, capture_output=True)

        if process.returncode != 0:  # Compilation error
            return False, process.stderr
        return True, None