import win32gui
import win32api
import win32con
import keyboard
import time


def click(hwnd, x, y):
    oldpos = win32api.GetCursorPos()

    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    time.sleep(0.001)
    win32api.SetCursorPos(oldpos)


def call_lane(hotkeys: list, hwnd_main: int, lane: str):
    global delay

    click_point = get_click_point(hwnd_main)

    # unpress all hotkeys to write the message
    for key in hotkeys:
        keyboard.release(key)

    # click into the chat window
    click(hwnd_main, click_point[0], click_point[1])

    # write the lane and send the message
    for c in lane:
        keyboard.press_and_release(c)

    keyboard.press_and_release("enter")

    # repress the hotkeys to return to previous keyboard state
    for key in hotkeys:
        keyboard.press(key)

    print("Called Lane:", lane)
    print("Waiting for input...")
    time.sleep(delay)


def get_click_point(hwnd):
    # window dimensions and position
    rect = win32gui.GetWindowRect(hwnd)
    winx = rect[0]
    winy = rect[1]

    # chat window dimensions
    w, h = 450, 50

    # chat window position
    x, y = 30, 1000

    # click point is in the middle of the chat
    clickx = x + int(w/2)
    clicky = y + int(h/2)

    return winx + clickx, winy + clicky


hotkeylanes = {
    "top": ["alt", "i"],
    "jgl": ["alt", "j"],
    "mid": ["alt", "k"],
    "adc": ["alt", "l"],
    "supp": ["alt", "o"],
    "bot pre": ["alt", "p"]
}
quitkeys = ["ctrl", "alt", "q"]
delay = 0.05

window_pollrate = 0.5


def main():
    global hotkeylanes, quitkeys

    quitkeystr = "+".join(quitkeys)

    hwnd_main = 0
    while not hwnd_main:
        hwnd_main = win32gui.FindWindow(None, "League of Legends")
        time.sleep(window_pollrate)

    print("Found League of Legends!")
    print("Waiting for input...")

    for lane, hotkeys in hotkeylanes.items():
        keyboard.add_hotkey("+".join(hotkeys), call_lane, args=(hotkeys, hwnd_main, lane))

    keyboard.wait(quitkeystr)

    return 0


if __name__ == "__main__":
    main()
