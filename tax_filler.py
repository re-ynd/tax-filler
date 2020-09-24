 #! python3

import pyautogui 
import time
import sys

scale = 2

type_duration = 0.02 * scale
tab_duration = 0.2 * scale
mouse_duration = 0.5 * scale
double_click_duration = 0.25 * scale
click_button_delay = 0.5 * scale
schedule_delay = 2 * scale


def click_button(button_label):
  print("Clicking on " + button_label + " button")
  count = 0
  button = None
  while count < 20 and button == None:
    time.sleep(click_button_delay)
    button = pyautogui.locateOnScreen(button_label + '.png')
    count += 1
  if not button:
    print("ERROR: Unable to find " + button_label + " button")
    sys.exit()
  pyautogui.click(button.left + button.width / 2, button.top + button.height / 2)
  time.sleep(click_button_delay)

def setup(schedule):
  pyautogui.doubleClick(10, 200, interval=double_click_duration)
  pyautogui.typewrite(["pageup"] * 20, interval=type_duration)
  click_button(schedule)
  pyautogui.doubleClick(10, 200, interval=double_click_duration)

def drop_select(index):
  print("Selecting dropdown " + index)
  pyautogui.typewrite(["pageup"] * 20, interval=type_duration)
  pyautogui.typewrite(["down"] * int(index), interval=type_duration)

def press_tab(count):
  if count == 0:
    return
  print("Tabbing " + tokens[0] + " times")
  if count < 0:
    pyautogui.keyDown('shift')
  pyautogui.typewrite('\t' * abs(count), interval=tab_duration)
  if count < 0:
    pyautogui.keyUp('shift')
  time.sleep(tab_duration)

def enter_data(tokens):
  tab_count = int(tokens[0])
  press_tab(tab_count)

  data = tokens[1]
  if data.startswith(">"):
    arg = data.split(' ', 1)[1]
    if data.startswith(">click "):
      click_button(arg)
    elif data.startswith(">drop "):
      drop_select(arg)
    elif data.startswith(">press "):
      print("Pressing " + arg)
      pyautogui.typewrite([arg], interval=type_duration)
    elif data.startswith(">sleep "):
      print("Sleeping for " + arg + " seconds")
      time.sleep(float(arg))
    elif data.startswith(">type "):
      print("Typing " + arg)
      pyautogui.typewrite(arg, interval=tab_duration)
  else:
    print("Typing " + data)
    pyautogui.typewrite(data)


if len(sys.argv) != 2:
  print('Usage: ' + sys.argv[0] + ' <data file>')
  sys.exit(1)

file = open(sys.argv[1])
for line in file:
  line = line.strip()
  if line.startswith(">schedule"):
    setup(line[1:])

  tokens = line.split(",", 1)
  if len(tokens) != 2:
    continue

  enter_data(tokens)
file.close()
