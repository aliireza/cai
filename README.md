# CodeAI (CAI): Code Optimization & Enhancement with AI [![Python Application](https://github.com/aliireza/cai/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/aliireza/cai/actions/workflows/ci.yml)

CodeAI (CAI) is a Python program designed to optimize and enhance your C/C++ code. It leverages Large Language Models (LLMs) to automate code transformations, ensuring that the output code maintains its compilability, correctness, and performance. It can interact with Google BARD, OpenAI's GPT, and Microsoft Bing APIs. 

**You should use a US VPN to interact with the BARD API (i.e., it is not supported in Sweden).**

## Key Features:

- **Automated Code Optimization:** CAI utilizes AI to refactor and optimize your existing code, potentially leading to more efficient and performant output.

- **Compilability Assurance:** The transformed code is ensured to be compilable.

- **Correctness Verification:** CAI verifies the functional equivalence of the original and transformed codes.

- **Performance Measurement:** The application benchmarks and compares the performance of the original and transformed code, ensuring that the changes have improved performance.


## How to Use:

You can use the application by running the following command:
```bash
python cai.py -i <input_file> -o <output_file> -t <task> -l <language> -a <AI API> -c -comp <compiler>
```

Where:

- `<input_file>` is the path to the original code.
- `<output_file>` is the path where the transformed code will be saved.
- `<task>` is the task you want the AI to perform on the code.
- `<language>` can be either C or C++.
- `<AI API>` is the name of the AI API to use; it can be BARD, GPT, or BING.
- `<compiler>` is the compiler to use for checking the compilability of the code, it can be gcc or g++.
For example:

```bash
python cai.py -i ../examples/2sum.cpp -o test.cpp -t "Improve the performance of the code and use the same main function as the original code" -l C++ -a BARD -c -comp gcc
```

**Note that you need to export `_BARD_API_KEY` and `OPENAI_API_KEY` variables in your operating system in order to use Bard and OpenAI's GPT. You can run the following command or add it to `.bashrc` or `.zshrc`:**

```bash
export _BARD_API_KEY="bard_api_key"
export OPENAI_API_KEY="openai_api_key"
```

**To use Bing, you should save the cookies in the `src/bing_cookies_1.json`. Check [Get API Key](#get-api-key) section for more information.**

## Get API Key

Check the following links for different LLMs:
- bardapi: https://github.com/dsdanielpark/Bard-API/blob/main/assets/bard_api.gif
- openai: https://platform.openai.com/account/api-keys 
- EdgeGPT: https://github.com/acheong08/EdgeGPT#chatbot

## Testing

You can test different classes by running the test units in the `tests/ folder, similar to the following command:

```bash
 python -m unittest test_ai_interface.py
```

**TODO: Currently, they are not working properly.**

## How to Build

You can build a python package using the following command:

```bash
python setup.py sdist bdist_wheel
```


## License

CodeAI is released under the [GPL 3.0 License](./LICENSE).
