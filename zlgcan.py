#!/usr/bin/python
#  zlgcan.py
#
#  ~~~~~~~~~~~~
#
#  ZLGCAN API
#
#  ~~~~~~~~~~~~
#
#  ------------------------------------------------------------------
#  Author : guochuangjian    
#  Last change: 25.12.2018
#
#  Language: Python 3.6
#  ------------------------------------------------------------------
#
from ctypes import *
import platform

INVALID_DEVICE_HANDLE = None
INVALID_CHANNEL_HANDLE = None

ZCAN_DEVICE_TYPE  = c_uint

ZCAN_PCI5121         = ZCAN_DEVICE_TYPE(1)
ZCAN_PCI9810         = ZCAN_DEVICE_TYPE(2)
ZCAN_USBCAN1         = ZCAN_DEVICE_TYPE(3)
ZCAN_USBCAN2         = ZCAN_DEVICE_TYPE(4)
ZCAN_PCI9820         = ZCAN_DEVICE_TYPE(5) 
ZCAN_CAN232          = ZCAN_DEVICE_TYPE(6)
ZCAN_PCI5110         = ZCAN_DEVICE_TYPE(7)
ZCAN_CANLITE         = ZCAN_DEVICE_TYPE(8)
ZCAN_ISA9620         = ZCAN_DEVICE_TYPE(9)
ZCAN_ISA5420         = ZCAN_DEVICE_TYPE(10)
ZCAN_PC104CAN        = ZCAN_DEVICE_TYPE(11)
ZCAN_CANETUDP        = ZCAN_DEVICE_TYPE(12)
ZCAN_CANETE          = ZCAN_DEVICE_TYPE(13)
ZCAN_DNP9810         = ZCAN_DEVICE_TYPE(14)
ZCAN_PCI9840         = ZCAN_DEVICE_TYPE(15)
ZCAN_PC104CAN2       = ZCAN_DEVICE_TYPE(16)
ZCAN_PCI9820I        = ZCAN_DEVICE_TYPE(17)
ZCAN_CANETTCP        = ZCAN_DEVICE_TYPE(18)
ZCAN_PCIE_9220       = ZCAN_DEVICE_TYPE(19)
ZCAN_PCI5010U        = ZCAN_DEVICE_TYPE(20)
ZCAN_USBCAN_E_U      = ZCAN_DEVICE_TYPE(21)
ZCAN_USBCAN_2E_U     = ZCAN_DEVICE_TYPE(22)
ZCAN_PCI5020U        = ZCAN_DEVICE_TYPE(23)
ZCAN_EG20T_CAN       = ZCAN_DEVICE_TYPE(24)
ZCAN_PCIE9221        = ZCAN_DEVICE_TYPE(25)
ZCAN_WIFICAN_TCP     = ZCAN_DEVICE_TYPE(26) 
ZCAN_WIFICAN_UDP     = ZCAN_DEVICE_TYPE(27)
ZCAN_PCIe9120        = ZCAN_DEVICE_TYPE(28)
ZCAN_PCIe9110        = ZCAN_DEVICE_TYPE(29)
ZCAN_PCIe9140        = ZCAN_DEVICE_TYPE(30)
ZCAN_USBCAN_4E_U     = ZCAN_DEVICE_TYPE(31)
ZCAN_CANDTU_200UR    = ZCAN_DEVICE_TYPE(32)
ZCAN_CANDTU_MINI     = ZCAN_DEVICE_TYPE(33)
ZCAN_USBCAN_8E_U     = ZCAN_DEVICE_TYPE(34)
ZCAN_CANREPLAY       = ZCAN_DEVICE_TYPE(35)
ZCAN_CANDTU_NET      = ZCAN_DEVICE_TYPE(36)
ZCAN_CANDTU_100UR    = ZCAN_DEVICE_TYPE(37) 
ZCAN_PCIE_CANFD_100U = ZCAN_DEVICE_TYPE(38)
ZCAN_PCIE_CANFD_200U = ZCAN_DEVICE_TYPE(39)
ZCAN_PCIE_CANFD_400U = ZCAN_DEVICE_TYPE(40)
ZCAN_USBCANFD_200U   = ZCAN_DEVICE_TYPE(41)
ZCAN_USBCANFD_100U   = ZCAN_DEVICE_TYPE(42)
ZCAN_USBCANFD_MINI   = ZCAN_DEVICE_TYPE(43)
ZCAN_CANFDCOM_100IE  = ZCAN_DEVICE_TYPE(44)
ZCAN_CANSCOPE        = ZCAN_DEVICE_TYPE(45)
ZCAN_CLOUD           = ZCAN_DEVICE_TYPE(46)
ZCAN_CANDTU_NET_400  = ZCAN_DEVICE_TYPE(47)
                    
ZCAN_VIRTUAL_DEVICE  = ZCAN_DEVICE_TYPE(99) 

ZCAN_STATUS_ERR         = 0
ZCAN_STATUS_OK          = 1
ZCAN_STATUS_ONLINE      = 2
ZCAN_STATUS_OFFLINE     = 3
ZCAN_STATUS_UNSUPPORTED = 4

ZCAN_TYPE_CAN           = c_uint(0)
ZCAN_TYPE_CANFD         = c_uint(1)

class ZCAN_DEVICE_INFO(Structure):
    _fields_ = [("hw_Version", c_ushort),
                ("fw_Version", c_ushort),
                ("dr_Version", c_ushort), 
                ("in_Version", c_ushort), 
                ("irq_Num", c_ushort),
                ("can_Num", c_ubyte),
                ("str_Serial_Num", c_ubyte * 20),
                ("str_hw_Type", c_ubyte * 40),
                ("reserved", c_ushort * 4)]

    def __str__(self):
        return '硬件版本号：V%d.%02d\r\n固件版本号：V%d.%02d\r\n驱动程序版本号：V%d.%02d\r\n接口库版本号：V%d.%02d\r\n' \
               '中断号：%s\r\nCAN通道数：%s\r\n序列号：%s\r\n硬件类型：%s' % ( \
                self.hw_Version / 0xFF, self.hw_Version & 0xFF,  \
                self.fw_Version / 0xFF, self.fw_Version & 0xFF,  \
                self.dr_Version / 0xFF, self.dr_Version & 0xFF,  \
                self.in_Version / 0xFF, self.in_Version & 0xFF,  \
                self.irq_Num, self.can_Num,  \
                ''.join(chr(c) for c in self.str_Serial_Num), 
                ''.join(chr(c) for c in self.str_hw_Type))

class _ZCAN_CHANNEL_CAN_INIT_CONFIG(Structure):
    _fields_ = [("acc_code", c_uint),
                ("acc_mask", c_uint),
                ("reserved", c_uint),
                ("filter",   c_ubyte),
                ("timing0",  c_ubyte),
                ("timing1",  c_ubyte),
                ("mode",     c_ubyte)]

class _ZCAN_CHANNEL_CANFD_INIT_CONFIG(Structure):
    _fields_ = [("acc_code",     c_uint),
                ("acc_mask",     c_uint),
                ("abit_timing",  c_uint),
                ("dbit_timing",  c_uint),
                ("brp",          c_uint),
                ("filter",       c_ubyte),
                ("mode",         c_ubyte),
                ("pad",          c_ushort),
                ("reserved",     c_uint)]

class _ZCAN_CHANNEL_INIT_CONFIG(Union):
    _fields_ = [("can", _ZCAN_CHANNEL_CAN_INIT_CONFIG), ("canfd", _ZCAN_CHANNEL_CANFD_INIT_CONFIG)]
 
class ZCAN_CHANNEL_INIT_CONFIG(Structure):
    _fields_ = [("can_type", c_uint),
                ("config", _ZCAN_CHANNEL_INIT_CONFIG)]

class ZCAN_CHANNEL_ERR_INFO(Structure):
    _fields_ = [("error_code", c_uint),
                ("passive_ErrData", c_ubyte * 3),
                ("arLost_ErrData", c_ubyte)]

class ZCAN_CHANNEL_STATUS(Structure):
    _fields_ = [("errInterrupt", c_ubyte),
                ("regMode",      c_ubyte),
                ("regStatus",    c_ubyte), 
                ("regALCapture", c_ubyte),
                ("regECCapture", c_ubyte),
                ("regEWLimit",   c_ubyte),
                ("regRECounter", c_ubyte),
                ("regTECounter", c_ubyte),
                ("Reserved",     c_ubyte)]

class ZCAN_CAN_FRAME(Structure):
    _fields_ = [("can_id",   c_uint, 29),
                ("err_flag", c_uint, 1),
                ("rtr_flag", c_uint, 1),
                ("eff_flag", c_uint, 1), 
                ("can_dlc",  c_ubyte),
                ("__pad",    c_ubyte),
                ("__res0",   c_ubyte),
                ("__res1",   c_ubyte),
                ("data",     c_ubyte * 8)]

class ZCAN_CANFD_FRAME(Structure): 
    _fields_ = [("can_id",    c_uint, 29), 
                ("err_flag",  c_uint, 1),
                ("rtr_flag",  c_uint, 1),
                ("eff_flag",  c_uint, 1), 
                ("len",       c_ubyte),
                ("brs_flag",  c_ubyte, 1),
                ("esi_flag",  c_ubyte, 1),
                ("res_flags", c_ubyte, 6),
                ("__res0",    c_ubyte),
                ("__res1",    c_ubyte),
                ("data",      c_ubyte * 64)]

class ZCAN_Transmit_Data(Structure):
    _fields_ = [("frame", ZCAN_CAN_FRAME), ("transmit_type", c_uint)]

class ZCAN_Receive_Data(Structure):
    _fields_  = [("frame", ZCAN_CAN_FRAME), ("timestamp", c_ulonglong)]

    def __str__(self):
        return "timestamp:%dus, can_id:0x%x, dlc:%d, eff:%d, rtr:%d, err:%d, data:%s" \
                % (self.timestamp, self.frame.can_id, self.frame.can_dlc, 
                self.frame.eff_flag, self.frame.rtr_flag, self.frame.err_flag, 
                ''.join((hex(self.frame.data[i]) + ' ') for i in range(self.frame.can_dlc)))

class ZCAN_TransmitFD_Data(Structure):
    _fields_ = [("frame", ZCAN_CANFD_FRAME), ("transmit_type", c_uint)]

class ZCAN_ReceiveFD_Data(Structure):
    _fields_ = [("frame", ZCAN_CANFD_FRAME), ("timestamp", c_ulonglong)]

    def __str__(self):
        return "timestamp:%dus, can_id:0x%x, dlc:%d, eff:%d, rtr:%d, brs:%d, esi:%d, err:%d, data:%s" \
                % (self.timestamp, self.frame.can_id, self.frame.len,  \
                self.frame.eff_flag, self.frame.rtr_flag, self.frame.brs_flag, \
                self.frame.esi_flag, self.frame.err_flag, 
                ''.join((hex(self.frame.data[i]) + ' ') for i in range(self.frame.len)))

class ZCAN_AUTO_TRANSMIT_OBJ(Structure):
    _fields_ = [("enable",   c_ushort),
                ("index",    c_ushort),
                ("interval", c_uint),
                ("obj",      ZCAN_Transmit_Data)]

class ZCANFD_AUTO_TRANSMIT_OBJ(Structure):
    _fields_ = [("enable",   c_ushort),
                ("index",    c_ushort),
                ("interval", c_uint),
                ("obj",      ZCAN_TransmitFD_Data)]

class IProperty(Structure):
    _fields_ = [("SetValue", c_void_p), 
                ("GetValue", c_void_p),
                ("GetPropertys", c_void_p)]

class ZCAN(object):
    def __init__(self):
        if platform.system() == "Windows":
            self.__m_dll = windll.LoadLibrary("zlgcan.dll")
            # self.__m_dll = cdll.LoadLibrary("zlgcan.dll")
        else:
            print("No support now!")
        if self.__m_dll == None:
            print("DLL couldn't be loaded!")

    def OpenDevice(self, device_type, device_index, reserved):
        try:
            return self.__m_dll.ZCAN_OpenDevice(device_type, device_index, reserved)
        except:
            print("OpenDevice Failed!")
            raise

    def CloseDevice(self, device_handle):
        try:
            return self.__m_dll.ZCAN_CloseDevice(device_handle)
        except:
            print("CloseDevice Failed!")
            raise

    def GetDeviceInf(self, device_handle):
        try:
            info = ZCAN_DEVICE_INFO()
            ret = self.__m_dll.ZCAN_GetDeviceInf(device_handle, byref(info))
            return info if ret == ZCAN_STATUS_OK else None
        except:
            print("Exception on ZCAN_GetDeviceInf")
            raise

    def DeviceOnLine(self, device_handle):
        try:
            return self.__m_dll.ZCAN_IsDeviceOnLine(device_handle)
        except:
            print("Exception on ZCAN_ZCAN_IsDeviceOnLine!")
            raise

    def InitCAN(self, device_handle, can_index, init_config):
        try:
            return self.__m_dll.ZCAN_InitCAN(device_handle, can_index, byref(init_config))
            # return CHANNEL_HANDLE(ret)
        except:
            print("Exception on ZCAN_InitCAN!")
            raise

    def StartCAN(self, chn_handle):
        try:
            return self.__m_dll.ZCAN_StartCAN(chn_handle)
        except:
            print("Exception on ZCAN_StartCAN!")
            raise

    def ResetCAN(self, chn_handle):
        try:
            return self.__m_dll.ZCAN_ResetCAN(chn_handle)
        except:
            print("Exception on ZCAN_ResetCAN!")
            raise

    def ClearBuffer(self, chn_handle):
        try:
            return self.__m_dll.ZCAN_ClearBuffer(chn_handle)
        except:
            print("Exception on ZCAN_ClearBuffer!")
            raise

    def ReadChannelErrInfo(self, chn_handle):
        try:
            ErrInfo = ZCAN_CHANNEL_ERR_INFO()
            ret = self.__m_dll.ZCAN_ReadChannelErrInfo(chn_handle, byref(ErrInfo))
            return ErrInfo if ret == ZCAN_STATUS_OK else None
        except:
            print("Exception on ZCAN_ReadChannelErrInfo!")
            raise

    def ReadChannelStatus(self, chn_handle):
        try:
            status = ZCAN_CHANNEL_STATUS()
            ret = self.__m_dll.ZCAN_ReadChannelStatus(chn_handle, byref(status))
            return status if ret == ZCAN_STATUS_OK else None
        except:
            print("Exception on ZCAN_ReadChannelStatus!")
            raise

    def GetReceiveNum(self, chn_handle, can_type = ZCAN_TYPE_CAN):
        try:
            return self.__m_dll.ZCAN_GetReceiveNum(chn_handle, can_type)
        except:
            print("Exception on ZCAN_GetReceiveNum!")
            raise

    def Transmit(self, chn_handle, std_msg, len):
        try:
            return self.__m_dll.ZCAN_Transmit(chn_handle, byref(std_msg), len)
        except:
            print("Exception on ZCAN_Transmit!")
            raise

    def Receive(self, chn_handle, rcv_num, wait_time = c_int(-1)):
        try:
            rcv_can_msgs = (ZCAN_Receive_Data * rcv_num)()
            ret = self.__m_dll.ZCAN_Receive(chn_handle, byref(rcv_can_msgs), rcv_num, wait_time)
            return rcv_can_msgs, ret
        except:
            print("Exception on ZCAN_Receive!")
            raise
    
    def TransmitFD(self, chn_handle, fd_msg, len):
        try:
            return self.__m_dll.ZCAN_TransmitFD(chn_handle, byref(fd_msg), len)
        except:
            print("Exception on ZCAN_TransmitFD!")
            raise
    
    def ReceiveFD(self, chn_handle, rcv_num, wait_time = c_int(-1)):
        try:
            rcv_canfd_msgs = (ZCAN_ReceiveFD_Data * rcv_num)()
            ret = self.__m_dll.ZCAN_ReceiveFD(chn_handle, byref(rcv_canfd_msgs), rcv_num, wait_time)
            return rcv_canfd_msgs, ret
        except:
            print("Exception on ZCAN_ReceiveFD!")
            raise

    def GetIProperty(self, device_handle):
        try:
            self.__m_dll.GetIProperty.restype = POINTER(IProperty)
            return self.__m_dll.GetIProperty(device_handle)
        except:
            print("Exception on ZCAN_GetIProperty!")
            raise

    def SetValue(self, iproperty, path, value):
        try:
            func = CFUNCTYPE(c_uint, c_char_p, c_char_p)(iproperty.contents.SetValue)
            return func(c_char_p(bytes(path, "utf-8")), c_char_p(bytes(value, "utf-8")))
        except:
            print("Exception on IProperty SetValue")
            raise

    def GetValue(self, iproperty, path):
        try:
            func = CFUNCTYPE(c_char_p, c_char_p)(iproperty.contents.GetValue)
            return func(c_char_p(bytes(path, "utf-8")))
        except:
            print("Exception on IProperty GetValue")
            raise

    def ReleaseIProperty(self, iproperty):
        try:
            return self.__m_dll.ReleaseIProperty(iproperty)
        except:
            print("Exception on ZCAN_ReleaseIProperty!")
            raise

def can_start(zcanlib, device_handle, chn):
    chn_init_cfg = ZCAN_CHANNEL_INIT_CONFIG()
    chn_init_cfg.can_type = ZCAN_TYPE_CANFD
    chn_init_cfg.config.canfd.abit_timing = 101166
    chn_init_cfg.config.canfd.dbit_timing = 101166
    chn_init_cfg.config.canfd.mode        = 0

    ip = zcanlib.GetIProperty(handle)
    zcanlib.SetValue(ip, str(chn) + "clock", "60000000")
    zcanlib.ReleaseIProperty(ip) 
 
    chn_handle = zcanlib.InitCAN(device_handle, chn, chn_init_cfg)
    if chn_handle is None:
        return None
    zcanlib.StartCAN(chn_handle)
    return chn_handle

if __name__ == "__main__":
    canfd_frame = ZCAN_ReceiveFD_Data()
    print(sizeof(canfd_frame))
    print(canfd_frame)
    zcanlib = ZCAN()
    handle = zcanlib.OpenDevice(ZCAN_USBCANFD_MINI, 0,0)
    print(handle)

    info = zcanlib.GetDeviceInf(handle)
    print(info)

    chn_handle = can_start(zcanlib, handle, 0)
    print(chn_handle)

    transmit_num = 100
    msgs   = (ZCAN_Transmit_Data * transmit_num)()
    for i in range(transmit_num):
        msgs[i].frame.can_id = i
        msgs[i].frame.can_dlc = 8
        for j in range(msgs[i].frame.can_dlc):
            msgs[i].frame.data[j] = j
        msgs[i].transmit_type = 2
    ret = zcanlib.Transmit(chn_handle, msgs, transmit_num)
    print("Tranmit Num: %d." % ret)

    while True:
        rcv_num = zcanlib.GetReceiveNum(chn_handle, ZCAN_TYPE_CAN)
        if rcv_num:
            print("Receive Num:%d" % rcv_num)
            rcv_msg = (ZCAN_Receive_Data * rcv_num)()
            rcv_msg, rcv_num = zcanlib.Receive(chn_handle, rcv_num)
            for i in range(rcv_num):
                print(rcv_msg[i])
        else:
            break
    zcanlib.ResetCAN(chn_handle)
    zcanlib.CloseDevice(handle)

