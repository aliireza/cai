import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='AI Code Generator and Verifier')
    parser.add_argument('-i', '--input', type=str, required=True, help='Input file path')
    parser.add_argument('-t', '--task', type=str, required=True, help='Task to be performed')
    parser.add_argument('-l', '--language', type=str, required=True, choices=['C', 'C++'], help='Language of the code')
    parser.add_argument('-a', '--ai', type=str, required=True, choices=['GPT', 'BARD', 'BING'], help='Choice of AI')
    parser.add_argument('-c', '--compile', action='store_true', help='Enable compilation check')
    parser.add_argument('-v', '--verify', action='store_true', help='Enable verification check')
    parser.add_argument('-p', '--performance', action='store_true', help='Enable performance check')
    parser.add_argument('-comp', '--compiler', type=str, required=True, choices=['gcc', 'clang'], help='Compiler to use')
    
    return parser.parse_args()