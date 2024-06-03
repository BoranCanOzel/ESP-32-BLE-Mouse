from SoftwareMouse import SoftwareMouse
import time


def test():
    while(1):
        time.sleep(1)
        mouse = SoftwareMouse(0, 0)
        mouse.MoveTo(100, 100)
        #mouse.Click(100, 100, 'left')
        #mouse.Release(100, 100, 'left')

test()