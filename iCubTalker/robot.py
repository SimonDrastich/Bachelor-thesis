from agentspace import Agent, Space
from noyarpicub import iCub_emotions
from iCubSim import iCubLimb
import yarp

yarp.Network.init()


class iCub(Agent):
    def __init__(self):
        app = '/main'
        self.head = iCubLimb(app, '/icubSim/head')
        self.left_arm = iCubLimb(app, '/icubSim/left_arm')
        self.right_arm = iCubLimb(app, '/icubSim/right_arm')
        self.left_leg = iCubLimb(app, '/icubSim/left_leg')
        self.right_leg = iCubLimb(app, '/icubSim/right_leg')
        self.torso = iCubLimb(app, '/icubSim/torso')
        self.limbs = {'head': self.head, 'torso': self.torso, 'left_arm': self.left_arm, 'right_arm': self.right_arm,
                      'left_leg': self.left_leg, 'right_leg': self.right_leg}
        self.emotions = iCub_emotions()

    def is_moving(self, target_position, limb):
        if self.limbs[limb].get() == target_position:
            return False
        return True
