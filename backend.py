from model import gpt3_completion,open_file
from ctrlSys import assistantCtrl

class Bot:
    conversation = list()
    def __init__(self):
        
        self.conversation.append({ 'role': 'system', 'content': open_file('prompt_chat.txt') })
    
    def get_response(self, message):

        content = message.encode(encoding='ASCII',errors='ignore').decode()
        self.conversation.append({"role": "user", "content": content})
                
        response = gpt3_completion(self.conversation)  
        response2 = assistantCtrl(message,response)

        self.conversation.append({"role": "assistant", "content": response2})
                    
        return response 

    def run(self):
            self.evieChat()



