import yarp
from iCubSim import iCubLimb
from noyarpicub import iCub_emotions 
yarp.Network.init()

app = '/renewer'

head = iCubLimb(app,'/icubSim/head')
head.set((0,0,0,0,0,0))

torso = iCubLimb(app,'/icubSim/torso')
torso.set((0,0,0))

left_arm = iCubLimb(app,'/icubSim/left_arm')
left_arm.set((0,80,0,50,0,0,0,59,20,20,20,10,10,10,10,10))

right_arm = iCubLimb(app,'/icubSim/right_arm')
right_arm.set((0,80,0,50,0,0,0,59,20,20,20,10,10,10,10,10))

left_leg = iCubLimb(app,'/icubSim/left_leg')
left_leg.set((0,0,0,0,0,0))

right_leg = iCubLimb(app,'/icubSim/right_leg')
right_leg.set((0,0,0,0,0,0))

emotions = iCub_emotions()
emotions.set('hap')

#right_arm.set(joint1=85,joint3=40,joint2=40)
