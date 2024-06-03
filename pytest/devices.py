from ctypes import *
from ctypes.wintypes import *
from structures import *
from constants import *
import ctypes

def errcheck(result,func,args):
    if result is None or result == -1:
        raise WinError(get_last_error())
    return result


user32 = WinDLL('user32', use_last_error=True)
RegisterRawInputDevices = user32.RegisterRawInputDevices
RegisterRawInputDevices.argtypes = (RawInputDevice * 7), UINT, UINT
RegisterRawInputDevices.restype = BOOL
RegisterRawInputDevices.errcheck = errcheck
GetRawInputData = user32.GetRawInputData
GetRawInputData.argtypes = INT, UINT, LPVOID, PUINT, UINT
GetRawInputData.restype = UINT
GetRawInputData.errcheck = errcheck

RegisterDevice = user32.RegisterRawInputDevices
RegisterDevice.argtypes = RawInputDevice, UINT, UINT
RegisterDevice.restype = BOOL
RegisterDevice.errcheck = errcheck


def register_devices(hwnd_target=None):
    page = 0x01
    # devices = (RawInputDevice * 7)(
    #     RawInputDevice(page, 0x01, DW_FLAGS, hwnd_target),
    #     RawInputDevice(page, 0x02, DW_FLAGS, hwnd_target),
    #     RawInputDevice(page, 0x04, DW_FLAGS, hwnd_target),
    #     RawInputDevice(page, 0x05, DW_FLAGS, hwnd_target),
    #     RawInputDevice(page, 0x06, DW_FLAGS, hwnd_target),
    #     RawInputDevice(page, 0x07, DW_FLAGS, hwnd_target),
    #     RawInputDevice(page, 0x08, DW_FLAGS, hwnd_target),
    # )
    # RegisterRawInputDevices(devices, len(devices), sizeof(devices[0]))

    devices = RawInputDevice(page, 0x02, DW_ExInputSink, hwnd_target)
    RegisterDevice(devices, 1, sizeof(devices))

    

def get_raw_input(handle):
    # dw_size = c_uint()
    # GetRawInputData(handle, RID_INPUT, None, byref(dw_size), sizeof(RawInputHeader))
    # lpb = LPBYTE(dw_size)
    # print(lpb.contents)
    # GetRawInputData(handle, RID_INPUT, lpb, byref(dw_size), sizeof(RawInputHeader))
    # print(lpb.contents)
    # return cast(lpb, POINTER(RawInput))
    
    dw_size = c_uint()
    GetRawInputData(handle, RID_INPUT, None, byref(dw_size), sizeof(RawInputHeader))
    
    # lpb = LPBYTE(dw_size)
    #print(dw_size)
    lpb = (ctypes.c_char *48)()
    # buffer = (ctypes.c_ubyte * 20)()

    # print(lpb.contents)
    GetRawInputData(handle, RID_INPUT, lpb, byref(dw_size), sizeof(RawInputHeader))
    # print(lpb.contents)
    return cast(lpb, POINTER(RawInput))
