#v1

import psutil
import win32gui
import win32process
import time

parent_pid = None
last_title = None
active = False

def find_parent():
    for p in psutil.process_iter(['pid', 'name']):
        if p.info['name'] == "RobloxStudioBeta.exe":
            return p.info['pid']
    return None

def get_window_titles_for_pid(target):
    titles = []
    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            if pid == target:
                title = win32gui.GetWindowText(hwnd)
                if title: titles.append(title)
        return True

    win32gui.EnumWindows(callback, None)
    return titles

while True:
    if parent_pid is None:
        parent_pid = find_parent()
        if parent_pid:
            print("Setting parent pid:", parent_pid)
        time.sleep(1)
        continue

    if not psutil.pid_exists(parent_pid):
        print("Studio closed")
        parent_pid = None
        last_title = None
        active = False
        time.sleep(1)
        continue

    titles  = get_window_titles_for_pid(parent_pid)
    current = titles[0] if titles else None

    if current != last_title:
        is_generic = current in (None, "Roblox Studio")
        was_generic = last_title in (None, "Roblox Studio")

        if was_generic and not is_generic:
            active = True
            print("Experience loaded, starting log:", current)
        elif not was_generic and is_generic:
            active = False
            print("Experience closed, stopping log")

        last_title = current

    time.sleep(1)