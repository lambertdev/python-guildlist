#!/usr/bin/env python
#coding: utf-8

import wx
import config
from wx.lib.wordwrap import wordwrap


        
        
def test():
    app = wx.PySimpleApp()
    frame = wx.Frame(None, -1, "A Frame", style=wx.DEFAULT_FRAME_STYLE,size=(200, 100))
    frame.Show()
    app.MainLoop()
    

if __name__ == '__main__':
    test()