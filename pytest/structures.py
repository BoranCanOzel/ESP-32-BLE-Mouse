from ctypes import Structure, windll, WINFUNCTYPE, c_int64, Union, c_byte, c_void_p
from ctypes.wintypes import *
from constants import *


HCURSOR = c_void_p


class RawInputDevice(Structure):
    _fields_ = [
        ("usUsagePage", USHORT),
        ("usUsage", USHORT),
        ("dwFlags", DWORD),
        ("hwndTarget", HWND),
    ]


class RawInputDeviceList(Structure):
    _fields_ = [
        ("hDevice", HANDLE),
        ("dwType", DWORD),
    ]


class RIDDeviceInfoHID(Structure):
    _fields_ = [
        ("dwVendorId", DWORD),
        ("dwProductId", DWORD),
        ("dwVersionNumber", DWORD),
        ("usUsagePage", USHORT),
        ("usUsage", USHORT),
    ]


class RIDDeviceInfo(Structure):
    _fields_ = [
        ("cbSize", DWORD),
        ("dwType", DWORD),
        ("hid", RIDDeviceInfoHID),
    ]


class WndClass(Structure):
    _fields_ = [
        ("style", UINT),
        ("lpfnWndProc", WNDPROC),
        ("cbClsExtra", INT),
        ("cbWndExtra", INT),
        ("hInstance", HINSTANCE),
        ("hIcon", HICON),
        ("hCursor", HCURSOR),
        ("hbrBackground", HBRUSH),
        ("lpszMenuName", LPCWSTR),
        ("lpszClassName", LPCWSTR),
    ]


class PaintStruct(Structure):
    _fields_ = [
        ("hdc", HDC),
        ("fErase", BOOL),
        ("rcPaint", RECT),
        ("fRestore", BOOL),
        ("fIncUpdate", BOOL),
        ("rgbReserved", BYTE * 32),
    ]


class RawInputHeader(Structure):
    _fields_ = [
        ("dwType", DWORD),
        ("dwSize", DWORD),
        ("hDevice", HANDLE),
        ("wParam", WPARAM),
    ]


class RawHID(Structure):
    _fields_ = [
        ("dwSizeHid", DWORD),
        ("dwCount", DWORD),
        ("bRawData", BYTE),
    ]


class MouseStruct(Structure):
    _fields_ = [
        ("usButtonFlags", USHORT),
        ("usButtonData", USHORT)
    ]


class MouseUnion(Union):
    _fields_ = [
        ("ulButtons", ULONG),
        ("data", MouseStruct)
    ]


class RawMouse(Structure):
    _fields_ = [
        ("usFlags", USHORT),
        ('usReseved', USHORT),
        ("data", MouseUnion),
        ("ulRawButtons", ULONG),
        ("lLastX", LONG),
        ("lLastY", LONG),
        ("ulExtraInformation", ULONG),
    ]


class RawKeyboard(Structure):
    _fields_ = [
        ("MakeCode", USHORT),
        ("Flags", USHORT),
        ("Reserved", USHORT),
        ("VKey", USHORT),
        ("Message", UINT),
        ("ExtraInformation", ULONG),
    ]


class RawUnion(Union):
    _fields_ = [
        ("mouse", RawMouse),
        ("keyboard", RawKeyboard),
        ("hid", RawHID)
    ]


class RawInput(Structure):
    _fields_ = [
        ("header", RawInputHeader),
        ("data", RawUnion),
    ]
    
class MSLLHOOKSTRUCT(Structure):
    _fields_ = (('pt',          POINT),
                ('mouseData',   DWORD),
                ('flags',       DWORD),
                ('time',        DWORD),
                ('dwExtraInfo', ULONG_PTR))