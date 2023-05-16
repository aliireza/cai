import bardapi
import openai
import os

class AIInterface:
    def __init__(self, ai_choice):
        self.ai_choice = ai_choice
        if ai_choice == 'BARD':
            self.bard_init()
        elif ai_choice == 'BING':
            pass
        elif ai_choice == 'GPT':
            pass
    
    def bard_init(self):
        os.environ['_BARD_API_KEY']="Vwhx8JyYA9-focLZk2ZYTLkzHH5I1cb5cRnkRFBBE_mxt9ADhffOxZoLNDyRFmruHwZ7Pw."
        bardapi.api_key = os.environ.get('_BARD_API_KEY', 'Not Set')
        self.bard = bardapi.core.Bard()

    def gpt_init(self):
        os.environ['OPENAI_API_KEY']="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"
        openai.api_key = os.environ.get('OPENAI_API_KEY', 'Not Set')
        self.gpt = openai()
        self.model="gpt-3.5-turbo"
        '''A temperature of 0 means the responses will be very straightforward, almost deterministic (meaning you almost always get the same response to a given prompt)
        A temperature of 1 means the responses can vary wildly.'''
        self.temperature=0

    def submit_task(self, task, code):
        if self.ai_choice == 'GPT':
            return self.submit_task_gpt(task, code)
        elif self.ai_choice == 'BARD':
            return self.submit_task_bard(task, code)
        elif self.ai_choice == 'BING':
            return self.submit_task_bing(task, code)
    
    #TODO: Check this function with the GPT API    
    def get_code_gpt(self, input):
        index = input.find("```")
        code = input[index:].strip()
        index = code.find("c++")
        code = code[index+3:].strip()
        index = code.find("```")
        code = code[:index].strip()
        return code
    
    #TODO: Check this function with the GPT API
    def submit_task_gpt(self, task, code):
        # Create a prompt 
        prompt = task + "\n" + code
        # Get response from GPT
        response = self.gpt.ChatCompletion.create(
        model=self.model,
        messages=prompt,
        temperature=self.temperature, 
    )
        # Extract the code from the response and return it 
        return self.get_code_gpt(response.choices[0].message["content"])

    def get_code_bard(self, input):
        index = input.find("```")
        code = input[index:].strip()
        index = code.find("c++")
        code = code[index+3:].strip()
        index = code.find("```")
        code = code[:index].strip()
        return code

    def submit_task_bard(self, task, code):
        # Create a prompt 
        prompt = task + "\n" + code
        # Get response from BARD
        response = self.bard.get_answer(prompt)
        # Extract the code from the response and return it 
        return self.get_code_bard(response.get('content'))

    def submit_task_bing(self, task, code):
        # Insert BING specific code here
        pass