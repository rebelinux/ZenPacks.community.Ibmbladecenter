# ==============================================================================
# IBMDeviceMap modeler plugin
#
# Zenoss community Zenpack for Avaya (Nortel) Devices
# version: 1.0
#
# (C) Copyright Jonathan Colon. All Rights Reserved.
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# ==============================================================================

__doc__ = """IBMDeviceMap
Use IBM BladeCenter Oid to determine hardware model + serial number as well
as OS information.
"""
__author__ = "Jonathan Colon"
__copyright__ = "(C) Copyright Jonathan Colon. 2011. All Rights Reserved."
__license__ = "GPL"
__version__ = "1.0.0"

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class IBMDeviceMap(SnmpPlugin):
    """Map mib elements from IBM mib to get hw and os products.
    """

    modname = "ZenPacks.community.Ibmbladecenter.IBMDevice"
    relname = "IBMDevice"
    maptype = "IBMDeviceMap"

    snmpGetMap = GetMap({
        '.1.3.6.1.4.1.2.3.51.2.2.21.1.1.3.0' : 'setHWSerialNumber',
        '.1.3.6.1.4.1.2.3.51.2.2.21.1.1.1.0' : 'setHWProductKey',
        '.1.3.6.1.4.1.2.3.51.2.2.21.1.1.2.0' : 'machinemodel',
        '.1.3.6.1.4.1.2.3.51.2.2.21.3.1.1.3.1' : 'setOSProductKey',
        })

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        if getdata['setHWProductKey'] is None: return None
        if getdata['setOSProductKey'] is None: return None
        om = self.objectMap(getdata)
        om.setOSProductKey = 'AMM Firmware ' + str(om.setOSProductKey)
        om.setHWProductKey = 'BladeCenter Model ' + str(om.machinemodel) + ' - Type ' + str(om.setHWProductKey)
        om.setHWProductKey = MultiArgs(om.setHWProductKey, "IBM")
        om.setOSProductKey = MultiArgs(om.setOSProductKey, "IBM")
        return om
