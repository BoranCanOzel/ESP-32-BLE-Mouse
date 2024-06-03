
from constants import *
from Comm import *

class SoftwareMouse:
    def __init__(self, x , y):
        self.curX = int(x)
        self.curY = int(y)
        self.mouseFlag = 0
        self.mouseData = 0
        self.deltaX = 0
        self.deltaY = 0

    def MoveTo(self, x, y):
        x = int(x)
        y = int(y)

        self.mouseFlag = 0
        self.mouseData = 0
        self.deltaX = x - self.curX
        self.deltaY = y - self.curY
        TransferData(self.mouseFlag, self.mouseData,self.deltaX, self.deltaY)
        self.curX = x
        self.curY = y
        print("({}, {}, {}, {})".format(self.curX, self.curY,self.deltaX, self.deltaY ))

    def Click(self, x, y, clickevent):
        x = int(x)
        y = int(y)
        
        if clickevent != 'left' and clickevent != 'right':
            return 
        if x != self.curX or y != self.curY:
            self.MoveTo(x, y)

        if clickevent == 'left':
            self.mouseFlag = LEFTBUTTON_DOWN
            self.mouseData = 0
        elif clickevent == 'right':
            self.mouseFlag = RIGHTBUTTON_DOWN
            self.mouseData = 0  
        
        TransferData(self.mouseFlag, self.mouseData,self.deltaX, self.deltaY)
             
            
    def Release(self, x, y, clickevent):
        x = int(x)
        y = int(y)
        
        if clickevent != 'left' and clickevent != 'right':
            return 
        if x != self.curX or y != self.curY:
            self.MoveTo(x, y)

        self.deltaX  = 0
        self.deltaY  = 0
        if clickevent == 'left':
            self.mouseFlag = LEFTBUTTON_UP
            self.mouseData = 0
        elif clickevent == 'right':
            self.mouseFlag = RIGHTBUTTON_UP
            self.mouseData = 0

        TransferData(self.mouseFlag, self.mouseData,self.deltaX, self.deltaY)    

    def wheel(self, scrollevent):
        if scrollevent != 'up' and scrollevent != 'down':
            return 
        
        self.deltaX = 0
        self.deltaY = 0
        if scrollevent == 'up':
            self.mouseData = SCROLL_UP
            self.mouseFlag = 0
        elif scrollevent == 'down':    
            self.mouseData = SCROLL_DOWN
            self.mouseFlag = 0

        TransferData(self.mouseFlag, self.mouseData,self.deltaX, self.deltaY)        
