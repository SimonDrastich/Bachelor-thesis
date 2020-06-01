import socket
import re
import sys
import types
import time

# parse respose from naming service
def get_addr(s):
    m = re.match("registration name [^ ]+ ip ([^ ]+) port ([0-9]+) type tcp",s)
    return (m.group(1),int(m.group(2))) if m else None
	
# get a single line of text from a socket
def getline(sock):
    result = ""
    while result.find('\n')==-1:
        result = result + sock.recv(1024).decode()
    result = re.sub('[\r\n].*','',result)
    return result
	
# send a message and expect a reply
def comm(addr,message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(addr)
    sock.send('CONNECT extern\n'.encode())
    getline(sock) 
    if isinstance(message, tuple):
        result=()
        for command in message:
            #print('SENT: ',command);
            sock.send(('d\n%s\n' % command).encode())
            result += (getline(sock),)
            #print('RECEIVED: ',result[-1]);
    else:
        sock.send(('d\n%s\n' % message).encode())
        result = getline(sock)
    sock.close()
    return result

class iCub_emotions:
    def __init__(self):
        self.host = 'localhost'
        port_name = '/emotion/in'
        self.query = get_addr(comm((self.host,10000),"query %s"%port_name))
        self.sock = socket .socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set('neu')

    def set(self, emotion='neu'):
        commands = ('set all '+emotion,)
        comm(self.query,commands)

if __name__ == "__main__":
    emotions = iCub_emotions()
    time.sleep(2)
    emotions.set("neu")
    time.sleep(2)
    emotions.set("hap")
    time.sleep(2)
    emotions.set("sad")
    time.sleep(2)
    emotions.set("sur")
    time.sleep(2)
    emotions.set("ang")
    time.sleep(2)
    emotions.set("evi")
    time.sleep(2)
    emotions.set("shy")
    time.sleep(2)
    emotions.set("cun")
    time.sleep(2)
    emotions.set("neu")
    
