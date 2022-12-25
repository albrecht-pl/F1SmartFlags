# F1 Smart Flags
Control your home automations based on F1 Race Flags by using simple screenshots and OCR.

<a href="https://www.buymeacoffee.com/alpl" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/arial-yellow.png" alt="Buy Me A Coffee" width="200px" ></a>
    <br />
    <br />
    Hey, I develop free and open source apps like this F1 race flag tracker. All donations are greatly appreciated and directly support my work.
  </p>

### Requirements
- Microsoft Windows
- Python 3.7 [(link)](https://www.python.org/downloads/release/python-370/)

### First time installation
- Clone this repository to a directory on your machine [how-to](https://help.github.com/desktop/guides/contributing/cloning-a-repository-from-github-to-github-desktop/).
- Start > cmd > cd to the source code directory.
- ```pip install -r requirements.txt```
- For the use with [Home Assistant](https://www.home-assistant.io/), you need to enable [API calls](https://developers.home-assistant.io/docs/api/rest/) and create an [Access Token](https://developers.home-assistant.io/docs/auth_api/#long-lived-access-token). Your Access Token has to be in the script.

### Usage
- Double click on 'F1SmartFlags.py' in Windows Explorer or run python F1SmartFlags.py from the command-line.
- The script checks a specific portion of the screen for Flag information, assuming, that the race is being watched in full-screen mode. See notes and thoughts for options about this.
- Enter the screen number, where F1 is watched, if prompted.

### Final notes, thoughts and acknowledgements
- The script was developed using the 2022 overlay during races, I will try to adjust to the next season ASAP, should there be noteworthy changes.
- The script should automatically adjust to different resolutions of 16:9 monitors and find the appropriate spot, where the Flags are shown. In case you're using different monitor sizes or don't watch the race in full-screen mode, you might have to find the coordinates for your own screen and correct the script. There is a debug function commented out, where the analyzed screenshot is shown, in order to adjust and find the right position.
- The home automation part in my case is Home Assistant. Adjust this for your own needs.
- I used the API calls to fire events on the Home Assistant event bus. This in turn can be used to trigger automations. Other options could include using a text helper and setting the text according to the Flag status or using a select helper and setting the selected option according to the status.
- At the time of writing this, the script is configured to wait 150 ms plus the runtime of about 50-100 ms per OCR cycle, before grabbing the screen again. To avoid false positives, a Flag detection is only sent out, if it occurred twice in a row. This leads to a delay of one cycle but insures more accurate readings. Change this for faster but potentially wrong readings, if needed.
- For Yellow Flags, the sectors are printed out in the script, but not differentiated, when the API call is sent. If you want the sectors to be sent out as well, differentiate accordingly. Due to the font used in the F1 overlay, the numbers are not always recognized correctly.
- Thanks to rr- for the [screeninfo](https://github.com/rr-/screeninfo) library.
