# -*- coding: ascii -*-
from __future__ import absolute_import, division, print_function  # v2.7 -> 3.5
"""
oooooooooooo       oooo oooo                    ooooo                 .o8
`888'     `8       `888 `888                    `888'                "888
 888       .ooooo.  888  888  .ooooo.  .oooo.o   888         .oooo.   888oooo.
 888oooo8 d88' `88b 888  888 d88' `88bd88(  "8   888        `P  )88b  d88' `88b
 888    " 888ooo888 888  888 888ooo888`"Y88b.    888         .oP"888  888   888
 888      888    .o 888  888 888    .oo.  )88b   888       od8(  888  888   888
o888o     `Y8bod8P'o888oo888o`Y8bod8P'8""888P'  o888ooooood8`Y888""8o `Y8bod8P'


@summary:      Felles lab parent classes
@author:       Sigve Karolius
@organization: Department of Chemical Engineering, NTNU, Norway
@contact:      sigveka@ntnu.no
@license:      Free (GPL.v3)
@requires:     Python 2.7.x or higher
@since:        18.06.2015
@version:      2.7
@todo 1.0:
@change:
@note:
"""
__author__  = "Sigve Karolius"
__email__   = "<firstname>ka<at>ntnu<dot>no"
__license__ = "GPL.v3"
__date__      = "$Date: 2015-06-23 (Tue, 23 Jun 2015) $"

from .SupportClasses import ExtendedRef, DataStorage
from .FellesBase import FellesBaseClass
from .GUI import FellesFrame, FellesButton, FellesTextInput, FellesLabel

from collections import defaultdict

# ================================ Class ==================================== #
class Controller(FellesBaseClass):
    """
    Syntactic sugar...
    """
    __controllers__ = defaultdict(list)
    # ------------------------------- Method -------------------------------- #
    def __init__(self, *args, **kwargs):
        super(Sensor, self).__init__(*args, **kwargs)
        self.__controllers__[self.__class__].append(ExtendedRef(self)) # Add instance to references

    # ------------------------------- Method -------------------------------- #
    @classmethod
    def InitGUI(cls):
        """
        Method creating sensor frames for the sensors
        """
        GUI = {}
        for ControllerType,Instances in cls.Instances():
            print("Creating GUI for Sensor: '%s'" %ControllerType.__class__.__name__)
            SensorGUI[ControllerType.__class__.__name__] = SensorFrame(
                                         sensors = Instances ,
                                         title = ControllerType.__class__.__name__ ,
                                         )

        return GUI

    # ------------------------------- Method -------------------------------- #
    def GetMeassurements(self):
        return self.module.get_analog_in()

    # ------------------------------- Method -------------------------------- #
    def __repr__(self):
        return '<%s.%s controller at %s>' % (
            self.__class__.__module__,
            self.__class__.__name__,
            self.ID
        )

# =============================== Class ====================================== #
class AlicatFrame(FellesFrame):


    """

                +------------------------------+ 
                |  |  Air  |  Sampl rate 0.5 ^ |
                |                Valve_Opening |
                |   T  298.0  K       |        |
                |   P    1.1  bar     |        |
                |   F   28.3  ml/s    o        |
                |   C    0.5  mg/L    |        |
                |                     -        |
                +------------------------------+

    """
    # ------------------------------- Method --------------------------------- #
    def __init__(self):
        """
        """
        self.resource = resource()
        super(AlicatFrame, self).__init__()

        self.InitUI()

    def InitUI(self):
        """
        """
        # Add a panel so it looks the correct on all platforms
        self.panel = wx.Panel(self, wx.ID_ANY)

        top_sizer = wx.BoxSizer(wx.VERTICAL) # Main sizer, all sizers are added
        title_sizer = wx.BoxSizer(wx.HORIZONTAL) # Contains "status"

        center_sizer = wx.BoxSizer(wx.HORIZONTAL) # Contains grid and valve
        valv_sizer = wx.BoxSizer(wx.VERTICAL) # 

        first_sizer = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer = wx.GridSizer(rows=4, cols=3, hgap=5, vgap=3)
        last_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create labels:
        self.title_sizer = FellesLabel(self.panel, label='Title')
        self.combo_box = FellesComboBox(self.panel, id=wx.ID_ANY,
                                         size=wx.DefaultSize,
                                         choices=self.resource.FLUIDS.keys(),
                                         style=wx.CB_DROPDOWN|wx.CB_READONLY,
                                         value="%s"%self.resource.GetGas(),
                                         source=self, target=self.SelectGas )

        self.smpl_speed = FellesTextInput(self.panel, value='%s' %1,
                                          initial=1, min=0, max=10,
                                          size=wx.Size(50,20),
                                          name='asdf',
                                          target=self.setSampleSpeed,
                                          arg='sample_speed',
                                          source=self )

        self.lble_speed = FellesLabel(self.panel, label='Sampling rate')
        self.valvLabel = FellesLabel(self.panel, label='Valve %')
        self.valvSlder = FellesSlider(self.panel, source=self, target=self.setFlowrate)

        self.labels = ['lables', 'Pressure', 'Temperature', 'Flow']
        self.Gridlabels = ['label', 'value', 'unit']
        self.Grid = { self.labels[0] : {
                   self.Gridlabels[0]:FellesLabel(self.panel, label='Variable'), 
                   self.Gridlabels[1]:FellesLabel(self.panel, label='Value'), 
                   self.Gridlabels[2]:FellesLabel(self.panel, label='Unit'),
                         } ,
                    self.labels[1] : { 
                self.Gridlabels[0]: FellesLabel(self.panel, label=self.labels[1]), 
                    self.Gridlabels[1]: FellesLabel(self.panel, label='0.00'), 
                    self.Gridlabels[2]: FellesLabel(self.panel, label='[bar]'),
                         } ,
                    self.labels[2] : { 
                self.Gridlabels[0]: FellesLabel(self.panel, label=self.labels[2]), 
                    self.Gridlabels[1]: FellesLabel(self.panel, label='0.00'), 
                    self.Gridlabels[2]: FellesLabel(self.panel, label='[K]'),
                         } ,
                    self.labels[3]: {
                self.Gridlabels[0]: FellesLabel(self.panel, label=self.labels[3]), 
                self.Gridlabels[1]: FellesLabel(self.panel, label='0.00'), 
                self.Gridlabels[2]: FellesLabel(self.panel, label='[cm^3/L]'),
                         } ,
                      }

        # Add labels to sizers:
        first_sizer.Add(self.combo_box, proportion=0, flag=wx.ALIGN_LEFT|wx.EXPAND, border=5)
        first_sizer.Add(wx.Size(90,25))
        first_sizer.Add(self.lble_speed, proportion=0, flag=wx.EXPAND|wx.ALIGN_RIGHT, border=5)
        first_sizer.Add(self.smpl_speed, proportion=0, flag=wx.ALIGN_RIGHT, border=5)

        valv_sizer.Add(self.valvLabel, proportion=0, flag=wx.CENTER, border=5)
        valv_sizer.Add(self.valvSlder, proportion=0, flag=wx.CENTER, border=5)

        for i,lab in enumerate(self.labels):
            for j,glab in enumerate(self.Gridlabels):
                if i ==0 or j == 0:
                    self.Grid[lab][glab].SetFont(wx.Font(pointSize=12, family=wx.MODERN, style=wx.NORMAL, weight=wx.BOLD, underline=False, faceName=u'Courier', encoding=wx.FONTENCODING_DEFAULT))

                grid_sizer.Add(self.Grid[lab][glab], proportion=0, flag=wx.ALL|wx.EXPAND, border=5)

        center_sizer.Add(grid_sizer, proportion=0, flag=wx.EXPAND, border=5)
        center_sizer.Add(valv_sizer, proportion=0, flag=wx.ALIGN_RIGHT, border=5)

        # Overall arrangement of the panel
        top_sizer.Add(title_sizer, proportion=0, flag=wx.CENTER|wx.EXPAND|wx.TOP)
        top_sizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, 5)
        top_sizer.Add(first_sizer, proportion=0, flag=wx.CENTER|wx.EXPAND, border=5)
        top_sizer.Add(center_sizer, proportion=0, flag=wx.ALL|wx.CENTER, border=5)
        top_sizer.Add(last_sizer, proportion=0, flag=wx.ALIGN_LEFT, border=5)

        # assigning the sizer to the panel
        self.panel.SetSizer(top_sizer)

        # fit the sizer to the panel
        self.top_sizer = top_sizer
        self.top_sizer.Fit(self)

    # ------------------------------- Method --------------------------------- #
    def UpdateFrame(self, sender=None, args=None):
        """
        Method for updating GUI
        """
        self.lables['label_speed'].SetLabel( '{num} {unit}'.format(
                                           num=self.Pump.data['data'][-1],
                                           unit=self.Pump['unit']),
                                           )

#        pub.sendMessage( 'Plot.%s' %self.GetLabel() )
        self.top_sizer.Layout()

    # ------------------------------- Method --------------------------------- #
    def setSampleSpeed(self, event):
        print(event)

    # ------------------------------- Method --------------------------------- #
    def setFlowrate(self, event):
        print(event)

    # ------------------------------- Method --------------------------------- #
    def SelectGas(self, event):
        self.resource.SetGas(event)

    # ------------------------------- Method --------------------------------- #
    def UpdateFrame(self, event):
        pass
