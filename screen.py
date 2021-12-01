import cv2
import numpy
import win32gui, win32ui, win32con

class Screen:
    def __init__(self, cornerX, cornerY, width, height):
        self.cornerX = cornerX
        self.cornerY = cornerY
        self.width = width
        self.height = height
        self.screen = None
        
    def updateScreen(self):
        screen = CaptureScreen((self.cornerX, self.cornerY), (self.width, self.height))
        screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2RGB)  #remove alpha channel        
        self.screen = screen
    
    def getScreen(self):
        if self.screen is None:
            self.updateScreen()
        return self.screen
    
    def showScreen(self, scale=1.0, duration=0):
        if self.screen is None:
            self.updateScreen()

        display = self.screen
        if scale != 1:
            display = cv2.resize(self.screen, (0, 0), fx=scale, fy=scale)
        cv2.imshow('screen', display)
        cv2.waitKey(duration)
        
    def __str__(self):
        return "Screen object: corner({0},{1}) | w,h: ({2},{3})".format(self.cornerX, self.cornerY, self.width, self.height)
    
    def updateDimensions(self, cornerX, cornerY, width, height):
        self.cornerX = cornerX
        self.cornerY = cornerY
        self.width = width
        self.height = height


def CaptureScreen(cornerPosition, dimensions):
    '''
    Code taken from https://stackoverflow.com/questions/41785831/how-to-optimize-conversion-from-pycbitmap-to-opencv-image
    :param cornerPosition: (tuple) x, y coordinate or the top left corner of screen roi
    :param dimensions: (tuple) width, height of screen roi
    :return: (ndarray) screen roi
    '''
    hwin = win32gui.GetDesktopWindow()
    width, height = dimensions
    cornerX = cornerPosition[0]
    cornerY = cornerPosition[1]
    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (cornerX, cornerY), win32con.SRCCOPY)

    signedIntsArray = bmp.GetBitmapBits(True)
    img = numpy.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return img


if __name__ == "__main__":
    screen = Screen(0, 0, 2560, 1440)
    screen.showScreen(duration=0, scale=0.75)
