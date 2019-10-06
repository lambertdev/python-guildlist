#!/usr/bin/env python
#coding: utf-8

#载入标准库
import wx
import os,sys
from wx.lib.wordwrap import wordwrap

try:
    from agw import ribbon as RB
except ImportError:
    import wx.lib.agw.ribbon as RB
    
#from wx.lib.embeddedimage import PyEmbeddedImage
from webbrowser import open_new
#程序库文件
import config

#程序开始
class MyTaskBarIcon(wx.TaskBarIcon):
    def __init__(self, frame,icon):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
        self.icon = icon
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnDoubleClick)
        self.Bind(wx.EVT_TASKBAR_RIGHT_DOWN, self.OnContextMenu)

    def OnDoubleClick(self, event):
        self.frame.Show()
        self.RemoveIcon()  

    def OnRightDown(self, event):
        self.frame.GramClose()

    def OnContextMenu(self, event):
        if not hasattr(self, "popupID"):
            self.popupID = wx.NewId()
            self.Bind(wx.EVT_MENU, self.OnRightDown, id=self.popupID)
        if not hasattr(self, "ABOUTDLG"):
            self.ABOUTDLG=wx.NewId()
            self.Bind(wx.EVT_MENU, self.frame.OnAboutDlg, id=self.ABOUTDLG)
        
        menu = wx.Menu()
        item = wx.MenuItem(menu, self.ABOUTDLG, u"About")
        menu.AppendItem(item)
        menu.AppendSeparator()
        item = wx.MenuItem(menu, self.popupID, u"退出")
        menu.AppendItem(item)
        
        self.PopupMenu(menu)
        menu.Destroy()
        
    def Set(self):
        self.SetIcon(self.icon, config.PROGRAMNAME+" "+config.VERSION)

class WMFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(900,600),style=wx.DEFAULT_FRAME_STYLE)
        self.rundir = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.imagedir = os.path.join(self.rundir,"images")
         
        self.icon = wx.EmptyIcon()
        iconimg = wx.Image(os.path.join(self.imagedir,"guildlist.ico"),wx.BITMAP_TYPE_ICO)
        iconimg.Rescale(32,32)
        self.icon.CopyFromBitmap(wx.BitmapFromImage(iconimg))
        self.SetIcon(self.icon)
         
        self.taskBarIcon=MyTaskBarIcon(self,self.icon)  
        self.Bind(wx.EVT_CLOSE, self.OnTaskBar)
         
        self.s = wx.BoxSizer(wx.VERTICAL)
        #self._logwindow = wx.TextCtrl(self, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize,wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_LEFT | wx.TE_BESTWRAP | wx.BORDER_NONE)

         
        self.ribbonBar()
        #s.Add(self._logwindow, 1, wx.EXPAND)
         
        #self.menuBar()
        #self.toolBar()
        self.SetSizer(self.s)
    
    def ribbonBar(self):
        self.ID_TB_NEW = wx.NewId()
        self.ID_TB_DEL_MEM = wx.NewId()
        self.ID_TB_EDIT =wx.NewId()
        self.ID_TB_GENE_PIC = wx.NewId()
        self.ID_TB_SAVE_AS = wx.NewId()
        self.ID_TB_EXIT = wx.NewId()
        self.ID_TB_ABOUT = wx.NewId()
        self.ID_TB_BROWSE = wx.NewId()
        
        self._ribbon = RB.RibbonBar(self, wx.ID_ANY)

        home = RB.RibbonPage(self._ribbon, wx.ID_ANY, "File")
        
        toolbar_panel = RB.RibbonPanel(home, wx.ID_ANY, u"Tools", wx.NullBitmap, wx.DefaultPosition,agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        tool_bar = RB.RibbonButtonBar(toolbar_panel, -1)
        tool_bar.AddSimpleButton(self.ID_TB_NEW, u'Add', wx.BitmapFromImage((wx.Image(os.path.join(self.imagedir, 'add.png'),wx.BITMAP_TYPE_PNG)).Rescale(48,48)),"")
        tool_bar.AddSimpleButton(self.ID_TB_EDIT,u'Edit', wx.BitmapFromImage((wx.Image(os.path.join(self.imagedir, 'edit.png'),wx.BITMAP_TYPE_PNG)).Rescale(48,48)),"")
        tool_bar.AddSimpleButton(self.ID_TB_DEL_MEM,u'Del', wx.BitmapFromImage((wx.Image(os.path.join(self.imagedir, 'del.png'),wx.BITMAP_TYPE_PNG)).Rescale(48,48)),"")
        tool_bar.AddSimpleButton(self.ID_TB_GENE_PIC, u"Redraw",wx.BitmapFromImage((wx.Image(os.path.join(self.imagedir, 'gene.png'),wx.BITMAP_TYPE_PNG)).Rescale(48,48)),"")
        tool_bar.AddSimpleButton(self.ID_TB_SAVE_AS, u"Save",wx.BitmapFromImage((wx.Image(os.path.join(self.imagedir, 'save.png'),wx.BITMAP_TYPE_PNG)).Rescale(48,48)),"")
        
        other_panel = RB.RibbonPanel(home, wx.ID_ANY,u"Other", wx.NullBitmap, wx.DefaultPosition,agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        other_bar = RB.RibbonButtonBar(other_panel, -1)
        other_bar.AddSimpleButton(self.ID_TB_EXIT, u"Exit", wx.BitmapFromImage((wx.Image(os.path.join(self.imagedir, 'exit.png'),wx.BITMAP_TYPE_PNG)).Rescale(48,47)),"")
        
        RB.RibbonPanel(home, wx.ID_ANY,"", wx.NullBitmap, wx.DefaultPosition,agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        
        help = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Help")
        
        about_panel = RB.RibbonPanel(help, wx.ID_ANY, "About", wx.NullBitmap, wx.DefaultPosition,agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        about_bar = RB.RibbonButtonBar(about_panel, -1)
        about_bar.AddSimpleButton(self.ID_TB_ABOUT,u"Help", wx.BitmapFromImage((wx.Image(os.path.join(self.imagedir, 'about.png'),wx.BITMAP_TYPE_PNG)).Rescale(48,48)),"")
        about_bar.AddSimpleButton(self.ID_TB_BROWSE, u"Browse",wx.BitmapFromImage((wx.Image(os.path.join(self.imagedir, 'browse.png'),wx.BITMAP_TYPE_PNG)).Rescale(48,48)),"")
        
        RB.RibbonPanel(help, wx.ID_ANY,"", wx.NullBitmap, wx.DefaultPosition,agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        
        self._ribbon.Realize()
        self.s.Add(self._ribbon, 0, wx.EXPAND)
      
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnAdd, id=self.ID_TB_NEW)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnSaveAs, id=self.ID_TB_SAVE_AS)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnEdit, id=self.ID_TB_EDIT)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnDelMem, id=self.ID_TB_DEL_MEM)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnRedraw, id=self.ID_TB_GENE_PIC)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnClose, id=self.ID_TB_EXIT)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnAboutDlg, id=self.ID_TB_ABOUT)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnBrowse, id=self.ID_TB_BROWSE)
        
    def toolBar(self):
        #self.ID_TB_NEW_GIRL = wx.NewId()
        #self.ID_TB_NEW_BOY = wx.NewId()
        self.ID_TB_NEW = wx.NewId()
        self.ID_TB_DEL_MEM = wx.NewId()
        self.ID_TB_EDIT =wx.NewId()
        self.ID_TB_GENE_PIC = wx.NewId()
        self.ID_TB_SAVE_AS = wx.NewId()
        self.ID_TB_EXIT = wx.NewId()
        
        self.toolbar = wx.ToolBar(self, -1, wx.DefaultPosition, wx.Size(48,48), wx.TB_HORIZONTAL|wx.TB_FLAT|wx.TB_TEXT)
        self.toolbar.SetToolBitmapSize(wx.Size (48, 48))
        
        #self.toolbar.AddLabelTool(self.ID_TB_NEW_GIRL, u'Add Girl'+'(&G)', wx.BitmapFromImage((wx.Image(os.path.join(self.imagedir, 'add_0.png'),wx.BITMAP_TYPE_PNG)).Rescale(48,48)), shortHelp=u'Add Gril',longHelp=u'Add Gril') 
        #self.toolbar.AddLabelTool(self.ID_TB_NEW_BOY, u'Add Boy'+'(&B)', wx.BitmapFromImage((wx.Image(os.path.join(self.imagedir, 'add_1.png'),wx.BITMAP_TYPE_PNG)).Rescale(48,48)), shortHelp=u'Add Boy',longHelp=u'Add Boy') 
        self.toolbar.AddLabelTool(self.ID_TB_NEW, u'Add'+'(&A)', wx.BitmapFromImage((wx.Image(os.path.join(self.imagedir, 'add.png'),wx.BITMAP_TYPE_PNG)).Rescale(48,48)), shortHelp=u'Add',longHelp=u'Add') 
        self.toolbar.AddLabelTool(self.ID_TB_EDIT, u'Edit'+'(&E)', wx.BitmapFromImage((wx.Image(os.path.join(self.imagedir, 'edit.png'),wx.BITMAP_TYPE_PNG)).Rescale(48,48)), shortHelp=u'EditMember', longHelp=u'Edit Member') 
        self.toolbar.AddLabelTool(self.ID_TB_SAVE_AS, u'Del'+'(&D)', wx.BitmapFromImage((wx.Image(os.path.join(self.imagedir, 'del.png'),wx.BITMAP_TYPE_PNG)).Rescale(48,48)), shortHelp=u'Delete Member', longHelp=u'Delete Member')
        self.toolbar.AddLabelTool(self.ID_TB_GENE_PIC, u"Redraw"+'(&R)', wx.BitmapFromImage((wx.Image(os.path.join(self.imagedir, 'gene.png'),wx.BITMAP_TYPE_PNG)).Rescale(48,48)), shortHelp=u"Redraw")  
        self.toolbar.AddLabelTool(self.ID_TB_GENE_PIC, u"Save"+'(&S)', wx.BitmapFromImage((wx.Image(os.path.join(self.imagedir, 'save.png'),wx.BITMAP_TYPE_PNG)).Rescale(48,48)), shortHelp=u"Save picture")  
        self.toolbar.AddLabelTool(self.ID_TB_EXIT, u"Exit"+'(&X)', wx.BitmapFromImage((wx.Image(os.path.join(self.imagedir, 'exit.png'),wx.BITMAP_TYPE_PNG)).Rescale(48,48)), shortHelp=u"Exit") 
        self.toolbar.Realize()
        self.SetToolBar(self.toolbar)
        
        #self.Bind(wx.EVT_TOOL, self.OnAddGirl, id=self.ID_TB_NEW_GIRL)
        #self.Bind(wx.EVT_TOOL, self.OnAddBoy, id=self.ID_TB_NEW_BOY)
        self.Bind(wx.EVT_TOOL, self.OnAdd, id=self.ID_TB_NEW)
        self.Bind(wx.EVT_TOOL, self.OnSaveAs, id=self.ID_TB_SAVE_AS)
        self.Bind(wx.EVT_TOOL, self.OnEdit, id=self.ID_TB_EDIT)
        self.Bind(wx.EVT_TOOL, self.OnDelMem, id=self.ID_TB_DEL_MEM)
        self.Bind(wx.EVT_TOOL, self.OnRedraw, id=self.ID_TB_GENE_PIC)
        self.Bind(wx.EVT_TOOL, self.OnClose, id=self.ID_TB_EXIT)
        
    def GramClose(self):
        self.taskBarIcon.Destroy()
        self.Destroy()
    
    def OnAddGirl(self,event):
        pass
    
    def OnAddBoy(self,event):
        pass
    
    def OnAdd(self,event):
        pass
    
    def OnSaveAs(self,event):
        pass
    
    def OnDelMem(self,event):
        pass
    
    def OnEdit(self,event):
        pass
    
    def OnRedraw(self,event):
        busy = wx.BusyInfo("Drawing,please wait...")
        wx.Yield()
        wx.MilliSleep(1000)
        busy.Destroy()
    
    def OnClose(self,event):
        self.taskBarIcon.Destroy()
        self.Destroy()
        
    def OnTaskBar(self,event):
        self.Show(False)
        self.taskBarIcon.Set()
         
    def OnAboutDlg(self,evnet):
        info = wx.AboutDialogInfo()
        info.Name = config.PROGRAMNAME
        info.Version = config.VERSION
        info.Copyright = config.COPYRIGHT
        info.Description = wordwrap(config.DESCRIPTION,350, wx.ClientDC(self))
        info.WebSite = (config.WEBSITE,config.WEBSITE)
        info.Developers = config.DEVELOPERS
        info.License = wordwrap("None", 500, wx.ClientDC(self))
        wx.AboutBox(info)
    
    def OnBrowse(self,event):
        open_new(config.WEBSITE) 