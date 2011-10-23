from Globals import InitializeClass
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.Device import Device
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from Products.ZenModel.ZenossSecurity import *
from copy import deepcopy

class IBMDevice(Device):
    "A IBM Device"


    _relations = Device._relations + (
        ('IBMBladeServer', ToManyCont(ToOne, 'ZenPacks.community.Ibmbladecenter.IBMBladeServer', 'IBMDevBladeServer')),
        )

    factory_type_information = deepcopy(Device.factory_type_information)

    def __init__(self, *args, **kw):
        Device.__init__(self, *args, **kw)
        self.buildRelations()

InitializeClass(IBMDevice)