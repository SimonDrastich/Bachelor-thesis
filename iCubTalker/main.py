from agentspace import Agent, Space
from receiver_server import ReceiverAgent
from lips import LipsAgent
from speak import speak
from rasa_core.agent import Agent as Chatbot
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.utils import EndpointConfig

import time
import unicodedata


class ListenerAgent(Agent):
    def     __init__(self, name):
        self.name = name
        self.chatbot_agent = self.loadChatbot()
        super().__init__()

##            ##
## DEBUG MODE ##  ovládanie pomocou terminálu:
##            ##

        # while True:
        #     user_input = input()
        #     user_input = user_input.lower()
        #     user_input = unicodedata.normalize('NFKD', user_input).encode('ASCII', 'ignore')
        #     responses = self.chatbot_agent.handle_text(user_input.decode('utf-8'))
        #     if responses:
        #         speak(responses[0]["text"])
        #         if (responses[0]["text"] == "Dobre, daj mi prosím chvíľu aby som sa to naučil" or responses[0][
        #             "text"] == "Malý moment, naučím sa to a nanovo načítam svoju neurónovú sieť"):
        #             time.sleep(12)
        #             self.chatbot_agent = self.loadChatbot()
        #     print("\n")

    def init(self):
        self.attach_trigger(self.name)

    def loadChatbot(self):
        nlu_model_path = "models/nlu/default/iCubbot"
        core_model_path = "models/dialogue"
        nlu_interpreter = RasaNLUInterpreter(nlu_model_path)
        action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
        return Chatbot.load(core_model_path, interpreter=nlu_interpreter, action_endpoint=action_endpoint)

    def senseSelectAct(self):
        text = Space.read(self.name, '')
        text = text.lower()
        text = str(unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore'))
        if len(text) <= 0 or text == "b'connect'":
            return
        print(text[2:-1])
        responses = self.chatbot_agent.handle_text(text)
        if responses:
            speak(responses[0]["text"])
            print("\n")
            if (responses[0]["text"] == "Dobre, daj mi prosím chvíľu aby som sa to naučil" or responses[0][
                "text"] == "Malý moment, naučím sa to a nanovo načítam svoju neurónovú sieť"):
                time.sleep(12)
                self.chatbot_agent = self.loadChatbot()


ReceiverAgent(7171, 'text')
LipsAgent('speaking')
ListenerAgent('text')
