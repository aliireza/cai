# CodeAI (CAI): Code Optimization & Enhancement with AI [![Python Application](https://github.com/aliireza/cai/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/aliireza/cai/actions/workflows/ci.yml)

A Python program that automatically changes an input C/C++ code, ensuring compilability, correctness, and performance.
You should use a US VPN to interact with the BARD API (i.e., it is not supported in Sweden).

## How to Use:

Example:
```bash
python3 cai.py -i ../examples/2sum.cpp -o test.cpp -t "Improve the performance of the code and use the same main function as the original code" -l C++ -a BARD -c -comp gcc
```

## Testing

Example
```bash
 python -m unittest test_ai_interface.py
```