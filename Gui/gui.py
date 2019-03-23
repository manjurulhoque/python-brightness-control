from tkinter import *
from ctypes import windll, byref, Structure, WinError, POINTER, WINFUNCTYPE
from ctypes.wintypes import BOOL, HMONITOR, HDC, RECT, LPARAM, DWORD, BYTE, WCHAR, HANDLE
from tkinter import messagebox
from Controller import *

MONITOR_ENUM_PROC = WINFUNCTYPE(BOOL, HMONITOR, HDC, POINTER(RECT), LPARAM)


class PhysicalMonitor(Structure):
    _fields_ = [('handle', HANDLE),
                ('description', WCHAR * 128)]


def iter_physical_monitors(close_handles=True):
    monitors = []

    def callback(hmonitor, hdc, pointer_rect, param):
        monitors.append(HMONITOR(hmonitor))
        return True

    if not windll.user32.EnumDisplayMonitors(None, None, MONITOR_ENUM_PROC(callback), None):
        raise WinError('EnumDisplayMonitors failed')

    for monitor in monitors:
        # Get physical monitor count
        count = DWORD()
        if not windll.dxva2.GetNumberOfPhysicalMonitorsFromHMONITOR(monitor, byref(count)):
            return WinError()
        # Get physical monitor handles
        physical_array = (PhysicalMonitor * count.value)()
        if not windll.dxva2.GetPhysicalMonitorsFromHMONITOR(monitor, count.value, physical_array):
            return WinError()
        for physical in physical_array:
            yield physical.handle
            if close_handles:
                if not windll.dxva2.DestroyPhysicalMonitor(physical.handle):
                    return WinError()


class Gui:
    def __init__(self, master):
        self.master = master
        self.label = None
        self.scale = None
        self.start()
        self.check_monitor_availability()
        self.create_widgets()

    def start(self):
        self.master.resizable(0, 0)
        self.master.title("Control Brightness")  # set title
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        # self.master.overrideredirect(1)  # Hide title bar

    def create_widgets(self):
        self.label = Label(self.master)
        self.label.config(font=("Courier", 16))
        self.label.grid(row=1, column=1)
        self.label.place(relx=0.16, rely=0.06, relwidth=0.7)

        self.scale = Scale(self.master)
        self.scale.grid(row=2, column=1)
        self.scale.place(relx=0.18, rely=0.3, relwidth=0.7)
        self.scale["variable"] = DoubleVar()
        self.scale["orient"] = HORIZONTAL
        self.scale["from_"] = 0
        self.scale["to"] = 100
        self.scale["command"] = self.print_value
        self.scale["sliderlength"] = 60
        self.scale["length"] = 350
        self.scale["width"] = 20
        for handle in iter_physical_monitors():
            self.scale.set(Brightness.brightness_value(handle, 0x10)[0])

        self.label.pack()
        self.scale.pack()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.master.destroy()

    def print_value(self, value):
        self.label.config(text="Current value: " + str(value), font=("Courier", 16))
        for monitor in iter_physical_monitors():
            Brightness.set_vcp_feature(monitor, 0x10, int(value))

    def close_windows(self):
        self.master.destroy()

    @staticmethod
    def check_monitor_availability():
        monitors = iter_physical_monitors()
        if isinstance(monitors, Exception):
            print("Something wrong")
            exit(0)
