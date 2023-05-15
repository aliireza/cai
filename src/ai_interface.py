class AIInterface:
    def __init__(self, ai_choice):
        self.ai_choice = ai_choice

    def submit_task(self, task, code):
        if self.ai_choice == 'GPT':
            return self.submit_task_gpt(task, code)
        elif self.ai_choice == 'BARD':
            return self.submit_task_bard(task, code)
        elif self.ai_choice == 'BING':
            return self.submit_task_bing(task, code)

    def submit_task_gpt(self, task, code):
        # Insert GPT specific code here
        pass

    def submit_task_bard(self, task, code):
        # Insert BARD specific code here
        pass

    def submit_task_bing(self, task, code):
        # Insert BING specific code here
        pass