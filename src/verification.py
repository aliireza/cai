import subprocess

class Verification:
    def __init__(self, verification_type):
        self.code = None
        self.prompt = "Your task is to create a C++ application to run symbolic execution using KLEE on two C++ functions and ensure they are equivalent; you should use assert for the equivalence check. I will provide you with two C++ functions (original code and improved code), and you should only return the full code (including the functions, a wrapper function, and main()) to be able to run KLEE. no text, please; give me the code only. no extern C"

    def verify(self, compiler, ai, original_code, generated_code):
        if(self.code is None):
            self.generate_code(compiler, ai, original_code, generated_code)
        return self.se_verification(compiler, original_code, generated_code)

    def generate_code(self, compiler, ai, original_code, generated_code):
        input_compilable = False
        self.prompt = self.prompt + "\n\\original code\n"+original_code + "\n\\improved code\n" + generated_code
        self.code = ai.submit_task( self.prompt, self.code)
        compile_task = "If there is not main; add it and use this code. If there is compilation erros, fix all of them: "
        
        while not input_compilable:
            compilable, error = compiler.compile_code(self.code, SE=1, output='klee_code.bc')
            print((error))
            if not compilable:
                self.code = ai.submit_task(compile_task + error, self.code)
                continue
            input_compilable = True

    def se_verification(self, compiler, original_code, generated_code):
        klee_command = [ 'klee', 'klee_code.bc']
        process = subprocess.run(klee_command, text=True, capture_output=True)
        if process.returncode != 0:  # Compilation error
            return False, process.stderr
        return True, None