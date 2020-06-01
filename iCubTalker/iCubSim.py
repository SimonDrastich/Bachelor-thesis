import yarp
import numpy as np
import cv2

class iCubLimb:
    def __init__(self,app_name,port_name):
        # prepare a property object
        self.props = yarp.Property()
        self.props.put('device','remote_controlboard')
        self.props.put('local',app_name+port_name)
        self.props.put('remote',port_name)
        # create remote driver
        self.armDriver = yarp.PolyDriver(self.props)
        # query motor control interfaces
        self.iPos = self.armDriver.viewIPositionControl()
        #self.iVel = self.armDriver.viewIVelocityControl()
        self.iEnc = self.armDriver.viewIEncoders()
        # retrieve number of joints
        self.jnts = self.iPos.getAxes()
        print('Controlling', self.jnts, 'joints of', port_name)
        
    def get(self):
        # read encoders
        encs = yarp.Vector(self.jnts)
        self.iEnc.getEncoders(encs.data())
        values = ()
        for i in range(self.jnts):
            values += (encs.get(i),)
        return values
        
    def set(self,values=(), \
        joint0=None,joint1=None,joint2=None,joint3=None,joint4=None,joint5=None,joint6=None,joint7=None, \
        joint8=None,joint9=None,joint10=None,joint11=None,joint12=None,joint13=None,joint14=None,joint15=None):
        # read encoders
        encs = yarp.Vector(self.jnts)
        self.iEnc.getEncoders(encs.data())
        # adjust joint positions
        for i in range(min(self.jnts,len(values))):
            if values[i] != None:
                encs.set(i,values[i])
        for i in range(16):
            value = eval('joint'+str(i))
            if value != None:
                print('joint',i,'=',value)
                encs.set(i,value)
        # write to motors
        self.iPos.positionMove(encs.data())
        
    def size(self):
        # return number of joints
        return self.jnts

class iCubCamera:
    def __init__(self,app_name,port_name):
        # open recipient port
        self.port = yarp.Port()
        self.port.open(app_name+port_name)
        yarp.delay(0.25)
        # connect the port to camera
        yarp.Network.connect(port_name,app_name+port_name)
        yarp.delay(0.25)
        # prepare data buffer for reception
        self.width = 320
        self.height = 240
        self.yarp_img = yarp.ImageRgb()
        self.yarp_img.resize(self.width,self.height)
        self.array_img = bytearray(self.width*self.height*3)
        self.yarp_img.setExternal(self.array_img,self.width,self.height)
        # prepare blank image to be returned when an error appears
        self.blank = np.zeros(self.shape())

    def grab(self):
        # receive one image
        self.port.read(self.yarp_img)
        # check if the image is correct
        if self.yarp_img.height() == self.height and self.yarp_img.width() == self.width:
            # turn the image to openCV format
            img = np.frombuffer(self.array_img, dtype=np.uint8)
            img = img.reshape(self.height,self.width,3)
            # correct its color model
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # return the OpenCV image
            return img
        else:
            return blank

    def shape(self): # can be called before any image is received
        # return shape of image provided by this camera 
        return (self.height,self.width,3)
        
