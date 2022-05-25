# Thank you GitHub user: angeloped! x
# https://gist.github.com/angeloped/3febaaf71ac083bc2cd5d99d775921d0
# Also thanks to: https://raspberrypi.stackexchange.com/a/2087

import sys
import os

def get_os() -> str:
    if "win" in sys.platform.lower():
        return "windows"

    elif "linux" in sys.platform.lower():
        return "linux"

    elif "darwin" in sys.platform.lower():
        return "darwin"

def get() -> str:

    # Get the device's operating system

    if get_os() == "windows":
        command = "wmic bios get serialnumber"
        return os.popen(command).read().split("\n")[2].strip(" ")

    elif get_os() == "linux":
        command = "cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2"
        return os.popen(command).read().strip("\n")

    elif get_os() == "darwin":
        command = "ioreg -l | grep IOPlatformSerialNumber"
        return os.popen(command).read().split("\"")[3]