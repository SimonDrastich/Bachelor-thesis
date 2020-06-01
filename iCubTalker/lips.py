from agentspace import Agent,Space
from noyarpicub import iCub_emotions 
import time
import random

class LipsAgent(Agent):

    def __init__(self,name):
        self.name = name
        super().__init__()
        
    def init(self):
        self.emotions = iCub_emotions()
        self.openmouth = False
        self.attach_timer(0.25)
 
    def senseSelectAct(self):
        speaking = Space.read(self.name,False)
        if speaking:
            if random.random() < 0.7:
                self.emotions.set('neu')
            else:
                self.emotions.set('sur')
                self.openmouth = True
        else:
            if self.openmouth:
                self.emotions.set('neu')
                self.openmouth = False

if __name__ == "__main__":
    LipsAgent('speaking')
    time.sleep(1.5)
    Space.write('speaking',True)
    time.sleep(3)
    Space.write('speaking',False)    

