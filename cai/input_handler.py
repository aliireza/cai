import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='Code AI (CAI)')
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='Input file path')
    parser.add_argument('-o', '--output', type=str, required=True,
                        help='Output file path')
    parser.add_argument('-t', '--task', type=str, required=True,
                        help='Task to be performed')
    parser.add_argument('-l', '--language', type=str, required=False,
                        choices=['C', 'C++'], default='C++',
                        help='Language of the code')
    parser.add_argument('-a', '--ai', type=str, required=False,
                        choices=['GPT', 'BARD', 'BING'], default='BARD',
                        help='Choice of AI')
    parser.add_argument('-c', '--compile', action='store_true', default=True,
                        help='Enable compilation check')
    parser.add_argument('-v', '--verify', action='store_true', default=False,
                        help='Enable verification check')
    parser.add_argument('-p', '--performance', action='store_true',
                        default=False, help='Enable performance check')
    parser.add_argument('-comp', '--compiler', type=str, required=False,
                        choices=['gcc', 'clang'], default='clang',
                        help='Compiler to use')

    args = parser.parse_args()
    # Correct the compiler based on the language:
    if args.language == 'C++':
        if args.compiler == 'gcc':
            args.compiler = 'g++'
        elif args.compiler == 'clang':
            args.compiler = 'clang++'
    return args


def read_code(filename):
    with open(filename, 'r') as file:
        code = file.read()
    return code
