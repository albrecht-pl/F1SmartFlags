####################################################
# DEBUG
####################################################

# import pyscreenshot

# pic = pyscreenshot.grab(bbox=(60,130,320,230))
# pic.show()

####################################################
# MAIN
####################################################

from screen_ocr import Reader
from screeninfo import get_monitors
import time
import json
from requests import post
from lightpack import lightpack

sleep_time = 150  # using milliseconds, adjust this to select repetition rate of ocr reading


def flashcolor(_color, _times):
    r = 0
    g = 0
    b = 0
    if _color == 'r':
        r = 255
    elif _color == 'y':
        r = 255
        g = 255
    else:
        g = 255

    for i in range(0, _times):
        lp.lock()
        if ledStatusFlag:
            lp.turnOn()
        lp.setColorToAll(0, 0, 0)
        lp.setColorToAll(r, g, b)
        time.sleep(0.3)
        lp.unlock()

        lp.lock()
        lp.setColorToAll(0, 0, 0)
        time.sleep(0.3)
        if ledStatusFlag:
            lp.turnOff()
        lp.unlock()


print("Flag Tracking Started.")
usage_mode = int(input('Choose operation mode: [1] Local, [2] Home Assistant, [3] Ambilight via Loopback\n')) - 1
if usage_mode not in range(0, 3):
    usage_mode = 0
    print("Selected option not recognized! Local operation.")
else:
    if usage_mode == 0:
        print("Selected operation mode: Local")
    elif usage_mode == 1:
        print("Selected operation mode: Home Assistant")
        with open('secrets.json') as json_data:
            data = json.load(json_data)
        url = "http://homeassistant.local:8123/api/events/F1Flag"
        headers = {
            "Authorization": data['Authorization'],
            "content-type": "application/json"
        }
    else:
        print("Selected operation mode: Ambilight via Loopback")
        with open('secrets.json') as json_data:
            data = json.load(json_data)
        lp = lightpack("127.0.0.1", data['port'], _apikey=data['apikey'])
        lp.connect()
        ledStatusFlag = False
        if lp.getStatus()[0:2] != "on":
            ledStatusFlag = True

        flashcolor('r', 1)
        flashcolor('y', 1)
        flashcolor('g', 1)

current_state = "Green"
state_changed = False

monitors = get_monitors()
if len(monitors) > 1:
    print('Found Monitors:')
    for index, monitor in enumerate(monitors):
        print(str(index + 1) + ": " + str(monitor))
    monitor_id = int(input('Enter the monitor number to watch: ')) - 1
    print('Watching Monitor: ' + str(monitor_id+1))
else:
    monitor_id = 0
x_min = int(60 / 1920 * monitors[monitor_id].width)
x_max = int(320 / 1920 * monitors[monitor_id].width)
y_min = int(130 / 1080 * monitors[monitor_id].height)
y_max = int(230 / 1080 * monitors[monitor_id].height)

ocr_reader = Reader.create_quality_reader()

while True:
    results = ocr_reader.read_screen([x_min, y_min, x_max, y_max])
    results_words = results.as_string()
    if results_words.__contains__("FLAG") or results_words.__contains__("SECTOR"):
        if results_words.__contains__('RED FLAG'):
            if current_state == "Red":
                if state_changed:
                    print("RED FLAG detected!")
                    state_changed = False
                    if usage_mode == 1:
                        event_type = "Red"
                        try:
                            response = post((url + event_type), headers=headers)
                            print(response.text)
                        except:
                            print("Home Assistant connection failed!")
                    elif usage_mode == 2:
                        flashcolor('r', 3)
            else:
                current_state = "Red"
                state_changed = True
        elif results_words.__contains__('GREEN FLAG'):
            if current_state == "Green":
                if state_changed:
                    print("GREEN FLAG detected!")
                    state_changed = False
                    if usage_mode == 1:
                        event_type = "Green"
                        try:
                            response = post((url + event_type), headers=headers)
                            print(response.text)
                        except:
                            print("Home Assistant connection failed!")
                    elif usage_mode == 2:
                        flashcolor('g', 3)
            else:
                current_state = "Green"
                state_changed = True
        else:
            if current_state == "Yellow":
                if state_changed:
                    results_words = results_words.split("\n")
                    print("YELLOW FLAG detected in " + results_words[1] + "!")
                    state_changed = False
                    if usage_mode == 1:
                        event_type = "Yellow"
                        try:
                            response = post((url + event_type), headers=headers)
                            print(response.text)
                        except:
                            print("Home Assistant connection failed!")
                    elif usage_mode == 2:
                        flashcolor('y', 3)
            else:
                current_state = "Yellow"
                state_changed = True
    elif results_words.__contains__("VIRTUAL") and (
            results_words.__contains__("SAFETY") or results_words.__contains__("CAR")):
        if current_state == "VSC":
            if state_changed:
                print("VSC Phase!")
                state_changed = False
                if usage_mode == 1:
                    event_type = "VSC"
                    try:
                        response = post((url + event_type), headers=headers)
                        print(response.text)
                    except:
                        print("Home Assistant connection failed!")
                elif usage_mode == 2:
                    flashcolor('y', 3)
        else:
            current_state = "VSC"
            state_changed = True
    elif results_words.__contains__("SAFETY") or results_words.__contains__("CAR"):
        if current_state == "SC":
            if state_changed:
                print("SAFETY CAR deployed!")
                state_changed = False
                if usage_mode == 1:
                    event_type = "SC"
                    try:
                        response = post((url + event_type), headers=headers)
                        print(response.text)
                    except:
                        print("Home Assistant connection failed!")
                elif usage_mode == 2:
                    flashcolor('y', 3)
        else:
            current_state = "SC"
            state_changed = True

    time.sleep(sleep_time / 1000)
