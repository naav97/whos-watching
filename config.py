import os
import platform

def get_extension_directories():
    system = platform.system()
    if system == "Windows":
        return [
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Extensions"),
            os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Extensions"),
        ]
    elif system == "Darwin":  # macOS
        return [
            os.path.expanduser("~/Library/Application Support/Google/Chrome/Default/Extensions"),
            os.path.expanduser("~/Library/Application Support/Firefox/Profiles"),
        ]
    elif system == "Linux":
        return [
            #os.path.expanduser("~/.config/google-chrome/Default/Extensions"),
            #os.path.expanduser("~/.mozilla/firefox"),
            os.path.expanduser("~/.config/BraveSoftware/Brave-Browser/Default/Extensions"),
        ]
    return []
