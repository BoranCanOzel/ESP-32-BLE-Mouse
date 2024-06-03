from ctypes import *
from ctypes.wintypes import *
from structures import *
from constants import *
import constants
from devices import get_raw_input, register_devices
import random
import sys
import os
import tkinter
import threading
import threading
from ttkbootstrap.constants import *
import win32api
import win32con
import ttkbootstrap as ttk
from Comm import *
import time


import mss
import numpy as np
import pyautogui
import subprocess

import pyautogui
from SoftwareMouse import *


def errcheck(result,func,args):
	if result is None or result == 0:
		raise WinError(get_last_error())
	return result


user32 = WinDLL('user32', use_last_error=True)
k32 = WinDLL('kernel32', use_last_error=True)
gdi32 = WinDLL('gdi32',use_last_error=True)
RegisterClass = user32.RegisterClassW
RegisterClass.argtypes = POINTER(WndClass),
RegisterClass.restype = ATOM
RegisterClass.errcheck = errcheck
CreateWindowEx = user32.CreateWindowExW
CreateWindowEx.argtypes = DWORD, LPCWSTR, LPCWSTR, DWORD, INT, INT, INT, INT, HWND, HMENU, HINSTANCE, LPVOID
CreateWindowEx.restype = HWND
CreateWindowEx.errcheck = errcheck
GetModuleHandle = k32.GetModuleHandleW
GetModuleHandle.argtypes = LPCWSTR,
GetModuleHandle.restype = HMODULE
GetModuleHandle.errcheck = errcheck
DefWindowProc = user32.DefWindowProcW
DefWindowProc.argtypes = HWND, UINT, WPARAM, LPARAM
DefWindowProc.restype = LRESULT
ShowWindow = user32.ShowWindow
ShowWindow.argtypes = HWND, INT
ShowWindow.restype = BOOL
UpdateWindow = user32.UpdateWindow
UpdateWindow.argtypes = HWND,
UpdateWindow.restype = BOOL
UpdateWindow.errcheck = errcheck
BeginPaint = user32.BeginPaint
BeginPaint.argtypes = HWND, POINTER(PaintStruct)
BeginPaint.restype = HDC
BeginPaint.errcheck = errcheck
FillRect = user32.FillRect
FillRect.argtypes = HDC, POINTER(RECT), HBRUSH
FillRect.restype = INT
FillRect.errcheck = errcheck
EndPaint = user32.EndPaint
EndPaint.argtypes = HWND, POINTER(PaintStruct)
EndPaint.restype = BOOL
EndPaint.errcheck = errcheck
PostQuitMessage = user32.PostQuitMessage
PostQuitMessage.argtypes = INT,
PostQuitMessage.restype = None
TranslateMessage = user32.TranslateMessage
TranslateMessage.argtypes = POINTER(MSG),
TranslateMessage.restype = BOOL
DispatchMessage = user32.DispatchMessageW
DispatchMessage.argtypes = POINTER(MSG),
DispatchMessage.restype = LRESULT
GetClientRect = user32.GetClientRect
GetClientRect.argtypes = HWND, POINTER(RECT)
GetClientRect.restype = BOOL
GetClientRect.errcheck = errcheck
GetMessage = user32.GetMessageW
GetMessage.argtypes = POINTER(MSG), HWND, UINT, UINT
GetMessage.restype = BOOL
DrawText = user32.DrawTextW
DrawText.argtypes = HDC, LPCWSTR, INT, POINTER(RECT), UINT
DrawText.restype = LRESULT
LoadIcon = user32.LoadIconW
LoadIcon.argtypes = HINSTANCE, LPCWSTR
LoadIcon.restype = HICON
LoadIcon.errcheck = errcheck
LoadCursor = user32.LoadCursorW
LoadCursor.argtypes = HINSTANCE, LPCWSTR
LoadCursor.restype = HCURSOR
LoadCursor.errcheck = errcheck
GetStockObject = gdi32.GetStockObject
GetStockObject.argtypes = INT,
GetStockObject.restype = HGDIOBJ
CreateSolidBrush = gdi32.CreateSolidBrush
CreateSolidBrush.argtypes = COLORREF,
CreateSolidBrush.restype = HBRUSH
TextOut = gdi32.TextOutW
TextOut.argtypes = HDC, INT, INT, LPCWSTR, INT
TextOut.restype = INT
SetBkMode = gdi32.SetBkMode
SetBkMode.argtypes = HDC, INT
SetBkMode.restype = INT
SetTextColor = gdi32.SetTextColor
SetTextColor.argtypes = HDC, COLORREF
SetTextColor.restype = COLORREF

SetWindowsHookExW = user32.SetWindowsHookExW
SetWindowsHookExW.errcheck = errcheck
SetWindowsHookExW.restype = HHOOK
SetWindowsHookExW.argtypes = (c_int,     # _In_ idHook
									 HOOKPROC,  # _In_ lpfn
									 HINSTANCE, # _In_ hMod
									 DWORD)     # _In_ dwThreadId

CallNextHookEx = user32.CallNextHookEx
CallNextHookEx.restype = LRESULT
CallNextHookEx.argtypes = (HHOOK,  # _In_opt_ hhk
								  c_int,  # _In_     nCode
								  WPARAM, # _In_     wParam
								  LPARAM) # _In_     lParam
LPMSLLHOOKSTRUCT = POINTER(MSLLHOOKSTRUCT)




right_clicked = 0

def LLMouseProc(nCode, wParam, lParam):
	
	global right_clicked 
	msg = cast(lParam, LPMSLLHOOKSTRUCT)[0]

	if nCode == HC_ACTION:
		msgid = MSG_TEXT.get(wParam, str(wParam))
		# msg = ((msg.pt.x, msg.pt.y),
		#         msg.mouseData, msg.flags,
		#         msg.time, msg.dwExtraInfo)
		# print('{:15s}: {}'.format(msgid, msg))

		if msgid == 'WM_LBUTTONDOWN' or msgid == 'WM_LBUTTONUP' or msgid == 'WM_RBUTTONDOWN' or msgid == 'WM_RBUTTONUP':
			#print("testing button is clicked")
			#print(msgid)
			if msgid == 'WM_RBUTTONDOWN':
				#SoftwareMouse.Click(self,0,0,"right")
				right_clicked = 1
			elif msgid == 'WM_RBUTTONUP':
				#SoftwareMouse.Release(0,0,"right")
				pass
			if msgid == 'WM_LBUTTONDOWN':
				#self.SoftwareMouse.Click(0,0,"left")
				right_clicked = 1
			elif msgid == 'WM_LBUTTONUP':
				#SoftwareMouse.Release(0,0,"left")

				pass
			if constants.BLOCK_SYSTEM == 0:

				return True # True means block
			else:
				return False
			

	return CallNextHookEx(None, nCode, wParam, lParam)


def window_callback(handle, message, w_param, l_param):
	if message == WM_INPUT:
		raw_input = get_raw_input(l_param)
		
		mouse_data = raw_input.contents.data.mouse
		
		deltaX = mouse_data.lLastX
		deltaY = mouse_data.lLastY

		uF = mouse_data.data.data.usButtonFlags
		ud = mouse_data.data.data.usButtonData
		
		#print(" ud : {}, uF : {}".format(ud, uF))
		TransferData(uF, ud, deltaX, deltaY)


	if win32api.GetAsyncKeyState(win32con.VK_ESCAPE):
		message == WM_DESTROY
		PostQuitMessage(0)
		constants.ACTIVE = 0
		start_button.configure(bg='teal')
		start_button.config(text="Enter Capture Mode")
		start_button.config(bg=original_color)
		return 0
	
	return DefWindowProc(handle, message, w_param, l_param)

def screenRes():
    # Get screen resolution
    with mss.mss() as sct:
        monitor = sct.monitors[1] # get the primary monitor, 0 returns total of them, 2 returns second monitor
        screen_width, screen_height = (monitor["width"], monitor["height"])
        #print(screen_width)

    # Calculate center of the screen
    center_x, center_y = screen_width // 2, screen_height // 2

    return center_x, center_y



def run():
	
	instance = GetModuleHandle(None)
	#class_name = 'TestWindow'
	class_name = 'TestWindow' + str(time.time())
	wnd = WndClass()
	wnd.style = CS_HREDRAW | CS_VREDRAW
	wnd.lpfnWndProc = WNDPROC(window_callback)
	wnd.hInstace = instance
	wnd.hCursor = 0#LoadCursor(None, IDC_ARROW)
	wnd.lpszClassName = class_name
	wnd.window_class = class_name

	RegisterClass(byref(wnd))
	#center_x, center_y = screenRes()
	
	handle = CreateWindowEx(
		0, class_name, 'Cursor Companion Window', WS_OVERLAPPEDWINDOW,
		0, 0, 200, 200,
		None, None, instance, None
	)
	
	
	#ShowWindow(handle, SW_NORMAL)
	UpdateWindow(handle)

	register_devices(handle)
	

	#set hook

	LowLevelMouseProc = HOOKPROC(LLMouseProc)

	SetWindowsHookExW(WH_MOUSE_LL, LowLevelMouseProc, None, 0)
	#print(constants.BLOCK_SYSTEM)
	if(constants.BLOCK_SYSTEM == 1):
		root2 = tkinter.Tk()
		root2.overrideredirect(True)
		root2.attributes('-topmost', True)
		root2.geometry('100x100')
		x, y = pyautogui.position()
		root2.geometry('%dx%d+%d+%d' % (100, 100, x - 50, y - 50))
		root2.update()


	global endflag
	msg = MSG()
	while GetMessage(byref(msg), None, 0, 0) != 0:
		if msg.message == 274:
			endflag = 1
		TranslateMessage(byref(msg))
		DispatchMessage(byref(msg))

		
		if(constants.BLOCK_SYSTEM == 1):
			x, y = pyautogui.position()
			root2.geometry('%dx%d+%d+%d' % (100, 100, x - 50, y - 50))
			root2.update()
			





def start():
	#print("startttttttttttttttttttt")
	global t
	t = threading.Thread(target=run)
	t.start()
	#import softwareMouseAccessTest
	

def stop():
	#ctypes.windll.user32.UnregisterClassW(wnd.window_class, None)
	#wnd.thread.join()
	#wnd.thread = None
	t.join()

def on_enter(e):
	global original_color
	if constants.ACTIVE == 0:
		original_color = ("medium aquamarine")
		start_button.config(bg='lightgray')

def on_leave(e):
	#print("LEAVEEEEEEEEEEEE")
	#print(constants.ACTIVE)
	if constants.ACTIVE == 0:
 		start_button.config(bg=original_color)

def on_click():
	start_button.config(bg='lightgray')

def change_input_mode():
	input_mode = constants.BLOCK_SYSTEM
	input_mode = input_mode + 1
	if input_mode > 2:
		input_mode = 0
	
	if input_mode == 0:
		mode_label.config(text="Input Mode: Block Mouse")
		constants.BLOCK_SYSTEM = 0
		
	elif input_mode == 1:
		mode_label.config(text="Input Mode: Cursor Companion")
		constants.BLOCK_SYSTEM = 1
	else:
		mode_label.config(text="Input Mode: No Block")
		constants.BLOCK_SYSTEM = 2


def trigger_functions():
	constants.ACTIVE = 1
	start_button.config(text="ACTIVE")
	#on_click()
	start()
	start_button.configure(bg='dark green')


def on_escape(e):
	if constants.ACTIVE == 0:
		start_button.configure(bg='teal')
		start_button.config(text="Enter Capture Mode")
		start_button.config(bg=original_color)
font1 = ('Helvlight', 10)
font2 = ('Helvlight', 8)
root = ttk.Window(themename="minty")

root.title("PythonP Link")
root.geometry("300x140")
frame = tkinter.Frame(root)
frame.pack()
button = tkinter.Label(frame, text="", width=0, height=1)
button.pack(side="top", fill="x", padx=5, pady=1)
start_button = tkinter.Button(frame, text="Enter Capture Mode",font=font1, height=3, width=20, command=trigger_functions)
start_button.pack(fill=tkinter.BOTH, expand=True)
start_button.configure(bg='medium aquamarine')
start_button.bind("<Enter>", on_enter)
start_button.bind("<Leave>", on_leave)
button = tkinter.Label(frame, text="Press escape to exit capture",font=font2, width=30, height=3)
button.pack(side="top", fill="x", padx=10, pady=1)
mode_label = tkinter.Label(frame, text="Input Mode: Block Mouse", font=font2, width=30, height=3)
mode_label.pack(side="top", fill="x", padx=10, pady=1)

# Define key bindings for changing input block mode
root.bind("<Tab>", lambda e: change_input_mode())
root.bind("<KP_Tab>", lambda e: change_input_mode())

root.bind("<Escape>", on_escape)
root.mainloop()



