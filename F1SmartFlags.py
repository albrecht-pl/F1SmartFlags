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
from requests import post

print("Flag Tracking Started.")

current_state = "Green"
state_changed = False
grab_rate = 150  # using milliseconds

url = "http://homeassistant.local:8123/api/events/F1Flag"
headers = {
    "Authorization": "Bearer XXXXXXXXX",
    "content-type": "application/json"
}
# replace Xs with your token

monitors = get_monitors()
if len(monitors) > 1:
    print('Found Monitors:')
    for index, monitor in enumerate(monitors):
        print(str(index + 1) + ": " + str(monitor))
    monitor_id = int(input('Enter the monitor number to watch: ')) - 1
else:
    monitor_id = 0
x_min = int(60/1920*monitors[monitor_id].width)
x_max = int(320/1920*monitors[monitor_id].width)
y_min = int(130/1080*monitors[monitor_id].height)
y_max = int(230/1080*monitors[monitor_id].height)

ocr_reader = Reader.create_quality_reader()

while True:
    results = ocr_reader.read_screen([x_min,y_min,x_max,y_max])
    results_words = results.as_string()
    if results_words.__contains__("FLAG") or results_words.__contains__("SECTOR"):
        if results_words.__contains__('RED FLAG'):
            if current_state == "Red":
                if state_changed:
                    print("RED FLAG detected!")
                    event_type = "Red"
                    response = post((url+event_type), headers=headers)
                    print(response.text)
                    state_changed = False
            else:
                current_state = "Red"
                state_changed = True
        elif results_words.__contains__('GREEN FLAG'):
            if current_state == "Green":
                if state_changed:
                    print("GREEN FLAG detected!")
                    event_type = "Green"
                    response = post((url+event_type), headers=headers)
                    print(response.text)
                    state_changed = False
            else:
                current_state = "Green"
                state_changed = True
        else:
            if current_state == "Yellow":
                if state_changed:
                    results_words = results_words.split("\n")
                    print("YELLOW FLAG detected in " + results_words[1] + "!")
                    event_type = "Yellow"
                    response = post((url+event_type), headers=headers)
                    print(response.text)
                    state_changed = False
            else:
                current_state = "Yellow"
                state_changed = True
    elif results_words.__contains__("VIRTUAL") and (results_words.__contains__("SAFETY") or results_words.__contains__("CAR")):
        if current_state == "VSC":
            if state_changed:
                print("VSC Phase!")
                event_type = "VSC"
                response = post((url+event_type), headers=headers)
                print(response.text)
                state_changed = False
        else:
            current_state = "VSC"
            state_changed = True
    elif results_words.__contains__("SAFETY") or results_words.__contains__("CAR"):
        if current_state == "SC":
            if state_changed:
                print("SAFETY CAR Phase!")
                event_type = "SC"
                response = post((url+event_type), headers=headers)
                print(response.text)
                state_changed = False
        else:
            current_state = "SC"
            state_changed = True

    time.sleep(grab_rate/1000)
