import abc
import bardapi
import openai
from EdgeGPT import Query, Cookie
from colorama import Fore, Style
import os
import sys


class AIInterface(abc.ABC):
    def __init__(self):
        self.init()

    @abc.abstractmethod
    def init(self):
        pass

    @abc.abstractmethod
    def submit_task(self, task, code, role=""):
        pass

    @abc.abstractmethod
    def get_code(self, response):
        pass


class Bard(AIInterface):
    def init(self):
        os.environ['_BARD_API_KEY'] = "Wwhx8AwK1QPvP3LnsV9Mxs1zu-vNzoaUUfbEimU3ZBKSMNuQ2-t06Cqe0RCTrTs7s7kT8A."
        bardapi.api_key = os.environ.get('_BARD_API_KEY', 'Not Set')
        self.bard = bardapi.core.Bard()

    def submit_task(self, task, code, role=""):
        # Create a prompt
        prompt = task + "\n" + code
        # Get response from BARD
        response = self.bard.get_answer(prompt)
        # Extract the code from the response and return it
        if ('Error' in response.get('content')):
            print(Fore.RED + "Error in BARD API." + Style.RESET_ALL)
            sys.exit(1)
        return self.get_code(response.get('content'))

    def get_code(self, response):
        index = response.find("```")
        code = response[index:].strip()
        index = code.find("c++")
        code = code[index+3:].strip()
        index = code.find("```")
        code = code[:index].strip()
        return code


class GPT(AIInterface):
    def init(self):
        os.environ['OPENAI_API_KEY'] = "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"
        openai.api_key = os.environ.get('OPENAI_API_KEY', 'Not Set')
        self.gpt = openai
        self.model = "gpt-3.5-turbo"
        '''A temperature of 0 means the responses will be very straightforward, almost deterministic (meaning you almost always get the same response to a given prompt)
        A temperature of 1 means the responses can vary wildly.'''
        self.temperature = 0
        self.submit_task("Always give me only code with syntax highlighting; for example ```c++ int main()```", "", "system")

    def submit_task(self, task, code, role="user"):
        # Create a prompt
        prompt = task + "\n" + code
        messages = [{"role": role, "content": prompt}]
        # Get response from GPT
        response = self.gpt.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,)
        # Extract the code from the response and return it
        if ('Error' in response):
            print(Fore.RED + "Error in OpenAI API." + Style.RESET_ALL)
            sys.exit(1)
        return self.get_code(response.choices[0].message["content"])

    def get_code(self, response):
        index = response.find("```")
        code = response[index:].strip()
        index = code.find("c++")
        code = code[index+3:].strip()
        index = code.find("```")
        code = code[:index].strip()
        return code


class Bing(AIInterface):
    def init(self):
        os.environ['BING_U'] = ""
        self.bing = Query
        self.style = "precise"  # creative, balanced, or precise
        self.content_type = "text"  # "text" for Bing Chat; "image" for Dall-e
        self.cookie_file = "./bing_cookies_1.json"
        c = Cookie()
        c.current_filepath = self.cookie_file
        c.import_data()
        # echo - Print something to confirm request made
        # echo_prompt - Print confirmation of the evaluated prompt

    def submit_task(self, task, code, role=""):
        # Create a prompt
        prompt = task + "\n" + code
        # Get response from Bing
        response = self.bing(prompt, self.style, self.content_type,
                             0, echo=False, echo_prompt=False)
        # Extract the code from the response and return it
        if ('Error' in response.output):
            print(Fore.RED + "Error in Bing API." + Style.RESET_ALL)
            sys.exit(1)
        return self.get_code(response)

    def get_code(self, response):
        return response.code


def AIBuilder(ai_choice):
    if ai_choice == 'BARD':
        return Bard()
    elif ai_choice == 'BING':
        return Bing()
    elif ai_choice == 'GPT':
        return GPT()
