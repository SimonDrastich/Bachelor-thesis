import os
import sys
import time
from agentspace import Agent,Space

def speak(text):
    print(text)
    filename = str(time.time())+'.txt'
    file = open(filename,'wb') 
    file.write(bytes(text,'utf-16')) 
    file.close() 
    os.environ["ESPEAK_DATA_PATH"] = "." 
    Space.write('speaking',True)
    os.system('espeak -v SK -b4 -f '+filename)
    os.remove(filename)
    Space.write('speaking',False)

if __name__ == "__main__":  
    text = sys.argv[1] if len(sys.argv) > 1 else "eee"
    speak(text)
    