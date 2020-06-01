import os
import sys
import time
from agentspace import Agent,Space
from lips import LipsAgent

def speak(text):
    os.environ["ESPEAK_DATA_PATH"] = "." 
    os.system('espeak -v SK "'+text+'"')

if __name__ == "__main__":  
    agent = LipsAgent('speaking')
    text = sys.argv[1] if len(sys.argv) > 1 else "eee"
    Space.write('speaking',True)
    print('speaking started')
    speak(text)
    print('speaking finished')
    Space.write('speaking',False)
    agent.stop()
    