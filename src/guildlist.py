#!/usr/bin/env python
#coding: utf-8

"This is main program,coding for water@moon dance guild \
Function:generate a simple list of guild members \
License:None \
Author:Lambert<lambertdev@gmail.com>"

import os, sys
import threading
import wx
import config
import wmframe

home = os.path.dirname(os.path.abspath(sys.argv[0]))

class GuildListSplash(wx.SplashScreen):
    def __init__(self,parent):
        global home
        self.parent = parent
        bmp = wx.Image(os.path.join(home, 'images', 'splash.png'),wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        wx.SplashScreen.__init__(self, bmp, wx.SPLASH_CENTER_ON_SCREEN|wx.SPLASH_TIMEOUT, 2000, None, -1)
        self.fc = wx.FutureCall(100, self.MainWindow)
        
    def MainWindow(self):
        self.frame = wmframe.WMFrame(None,-1,config.PROGRAMNAME+" "+config.VERSION)
        self.frame.CenterOnScreen()
        self.parent.SetTopWindow(self.frame)
        self.frame.Show(True)

class GuildList(wx.App):
    def __init__(self):
        wx.App.__init__(self, 0)
    def OnInit(self):
        splash = GuildListSplash(self)
        splash.Show(True)
        
        self.Bind(wx.EVT_ACTIVATE_APP, self.OnGramStart)  
        return True
    def OnGramStart(self,event):
        pass
    
def main():
    app = GuildList()
    app.MainLoop()
    


if __name__ == '__main__':
    main()