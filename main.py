import win32gui
import win32api
import win32con
import keyboard
import time
import sys


def click(hwnd, x, y):
    oldpos = win32api.GetCursorPos()

    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    time.sleep(0.001)
    win32api.SetCursorPos(oldpos)


def print_special(*x, end="\n"):
    """ prints in green """
    print("\033[92m", end="")
    for elem in x:
        print(str(elem), end=" ")
    print(end=end)
    print("\033[0m", end="")
    return


def get_green_text(x):
    """ returns green text """
    return "\033[92m{}\033[0m".format(x)


def reprint(*x, end="\n"):
    """ prints in same line """
    message = ""
    for elem in x:
        message += str(elem) + " "
    # \r prints a carriage return first, so `b` is printed on top of the previous line.
    sys.stdout.write("\r" + message[:-1])
    sys.stdout.flush()
    return


def call_lane(hotkeys: list, hwnd_main: int, lane: str):
    global delay

    click_point = get_click_point(hwnd_main)

    # unpress all hotkeys to write the message
    for key in hotkeys:
        keyboard.release(key)

    # if window is minimized, maximize it and bring it to the foreground
    if win32gui.IsIconic(hwnd_main):
        win32gui.ShowWindow(hwnd_main, 1)
        time.sleep(0.5)  # Maximizing the window takes a bit
    win32gui.SetForegroundWindow(hwnd_main)

    # click into the chat window
    click(hwnd_main, click_point[0], click_point[1])

    # write the lane and send the message
    for c in lane:
        keyboard.press_and_release(c)

    keyboard.press_and_release("enter")

    # repress the hotkeys to return to previous keyboard state
    for key in hotkeys:
        keyboard.press(key)

    # print_special(lane)

    reprint("Called Lane: ", get_green_text(lane))
    # print("Waiting for input...")
    time.sleep(delay)


def get_click_point(hwnd):
    # get window top left and bottom right positions and calculate dimensions
    rect = win32gui.GetWindowRect(hwnd)
    winx = rect[0]
    winy = rect[1]
    winw = rect[2] - winx
    winh = rect[3] - winy

    # relative center of the chat window
    x, y = 0.14, 0.95

    # calculate center of chat window
    clickx = winx + int(winw * x)
    clicky = winy + int(winh * y)

    return clickx, clicky


lane_hotkeys = {
    "top": ["alt", "i"],
    "jgl": ["alt", "j"],
    "mid": ["alt", "k"],
    "adc": ["alt", "l"],
    "supp": ["alt", "o"],
    "bot pre": ["alt", "p"],
}
quitkeys = ["ctrl", "alt", "q"]
delay = 0.05

window_pollrate = 0.5


def main():
    global lane_hotkeys, quitkeys

    quitkeystr = "+".join(quitkeys)

    print("Searching for League of Legends..", end="")
    hwnd_main = 0
    while not hwnd_main:
        hwnd_main = win32gui.FindWindow(None, "League of Legends")
        print(".", end="")
        sys.stdout.flush()
        time.sleep(window_pollrate)

    print(" Found!"
          "\nHotkeys:")

    for lane, hotkeys in lane_hotkeys.items():
        print("  {}: {}".format(get_green_text(lane.capitalize()), " + ".join([x.upper() for x in hotkeys])))

    sys.stdout.flush()

    for lane, hotkeys in lane_hotkeys.items():
        keyboard.add_hotkey("+".join(hotkeys), call_lane, args=(hotkeys, hwnd_main, lane))

    keyboard.wait(quitkeystr)

    return 0


if __name__ == "__main__":
    main()
