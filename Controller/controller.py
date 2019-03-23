from ctypes import windll, byref, WinError
from ctypes.wintypes import DWORD, BYTE, HANDLE


class Brightness:
    winID = windll.user32.GetForegroundWindow()
    MONITOR_DEFAULT_TO_NULL = 0
    MONITOR_DEFAULT_TO_PRIMARY = 1
    MONITOR_DEFAULT_TO_NEAREST = 2

    def __init__(self):
        self.current_monitor_id = 2  # Get current monitor ID

    @staticmethod
    def brightness_value(monitor, code):
        api_call = windll.Dxva2.GetVCPFeatureAndVCPFeatureReply
        api_in_vcp_code = BYTE(code)
        api_out_current_value = DWORD()
        api_out_max_value = DWORD()

        if not api_call(monitor, api_in_vcp_code, None,
                        byref(api_out_current_value),
                        byref(api_out_max_value)):
            print('get vcp command failed: ' + hex(code))
            raise WinError()
        return api_out_current_value.value, api_out_max_value.value

    @staticmethod
    def set_vcp_feature(monitor, code, value):
        if not windll.dxva2.SetVCPFeature(HANDLE(monitor), BYTE(code), DWORD(value)):
            raise WinError()
