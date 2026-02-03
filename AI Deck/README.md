# Getting Started with AI-Deck RGB (Wi-Fi Stream) + Color Blob Follow via Python

This tutorial shows you how to:

* Set up the AI-Deck Wi-Fi camera streamer from scratch
* Install the necessary host software
* Connect to the AI-Deck access point and verify video streaming
* Run a Python script that tracks a colored object and sends small yaw and forward commands to the Crazyflie

---

## What You Need

* Crazyflie 2.x
* AI-Deck (RGB camera + GAP8)
* Crazyradio PA (for command/control via `cflib`)
* Charged battery
* A laptop running macOS or Linux with Wi-Fi
* A safe test area (start on the ground, props off if possible)

---

## Step 1: Install Python 3

macOS:

```bash
brew install python
```

Ubuntu:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

Verify:

```bash
python3 --version
pip3 --version
```

---

## Step 2: Create a Virtual Environment

Create and activate a virtual environment:

```bash
mkdir -p ~/aideck-rgb-tutorial
cd ~/aideck-rgb-tutorial

python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -U pip
pip install opencv-python numpy cflib pupil-apriltags
```

---

## Step 3: Build and Flash the Wi-Fi Streamer (One-time)

You only do this once per AI-Deck firmware setup.

### 3.1 Get the AI-Deck GAP8 examples

Clone or download `aideck-gap8-examples` from Bitcraze (or use what you already have).

Move into the folder:

```bash
cd /path/to/aideck-gap8-examples
```

### 3.2 Build the Wi-Fi image streamer using Docker

```bash
docker run --rm -v ${PWD}:/module bitcraze/aideck \
  tools/build/make-example examples/other/wifi-img-streamer image
```

### 3.3 Flash the streamer to the GAP8

Edit the URI if needed:

```bash
cfloader flash \
  examples/other/wifi-img-streamer/BUILD/GAP8_V2/GCC_RISCV_FREERTOS/target.board.devices.flash.img \
  deck-bcAI:gap8-fw -w radio://0/80/2M
```

---

## Step 4: Enable AI-Deck Wi-Fi AP Mode (Crazyflie Firmware)

In the Crazyflie firmware configuration:

* Enable AI-Deck support
* Set AI-Deck Wi-Fi mode to **AP**
* Set SSID and KEY
* Build and flash Crazyflie firmware

Then:

1. Power-cycle the Crazyflie
2. Connect your laptop’s Wi-Fi to the AI-Deck SSID

Common default IP for the deck in AP mode is:

* `192.168.4.1`

---

## Step 5: Verify Streaming with the Official Viewer

Locate the official viewer script:

```
aideck-gap8-examples/examples/other/wifi-img-streamer/opencv-viewer.py
```

Run it (if needed, activate your venv first):

```bash
source ~/aideck-rgb-tutorial/venv/bin/activate
python3 /path/to/aideck-gap8-examples/examples/other/wifi-img-streamer/opencv-viewer.py
```

If it works, you should see an OpenCV window showing the live camera stream.

---

## Step 6: Set Up the Blob Follow Script

In your tutorial repo, create a `scripts/` folder and add the script:

```bash
cd ~/aideck-rgb-tutorial
mkdir -p scripts
```

Create `scripts/blob_follow.py` and paste your code into it.

Recommended: update the script so the radio URI is configurable via CLI:

* `--uri radio://0/80/2M`

(If you want, I can rewrite your script with clean CLI flags, safety clamps, and a steady send rate.)

---

## Step 7: Power On and Connect Everything

1. Plug the Crazyradio PA into your laptop
2. Connect the battery to the Crazyflie
3. Wait for LEDs
4. Connect your laptop Wi-Fi to the AI-Deck SSID
5. Place the drone on a flat surface

Safety note:

* First run it on the ground and watch the yaw response.
* Fly only after you can hover reliably and you understand how to stop the script fast.

---

## Step 8: Run the Blob Follower

Put a red object in view (example target: red cap).

Run:

```bash
source ~/aideck-rgb-tutorial/venv/bin/activate
python3 scripts/blob_follow.py --deck_ip 192.168.4.1
```

Optional HSV tuning:

```bash
python3 scripts/blob_follow.py \
  --deck_ip 192.168.4.1 \
  --hsv_lo 0 120 70 \
  --hsv_hi 10 255 255
```

To stop:

* Press `ESC` in the OpenCV window
* If needed, unplug the battery

---

## What It Does

The script:

* Receives frames from the AI-Deck over Wi-Fi
* Converts each frame to HSV
* Thresholds the image to isolate the target color
* Finds the largest blob
* Computes how far it is from the image center
* Sends yaw-rate commands to rotate toward the target
* Creeps forward when centered and not “close enough”

---

## Tuning Tips

You will likely need to tune:

* `hsv_lo` and `hsv_hi` for your lighting
* `K_yaw` (turn strength)
* `target_area` (how close is “close enough”)
* `deadband` (ignore tiny pixel errors)

Quick tuning trick:

* Start by getting a clean mask (good HSV bounds)
* Then add yaw control
* Then add forward motion last

---
## Attribution

This tutorial compiles and explains work by Arkajit and Cesar (original notes):

```text
https://docs.google.com/document/d/1_mckQ8RGXXScUb0hJiAWuo1YxMDqM7_c5HpG1ZoWX9I/edit?tab=t.0
```

## Additional resources

### Bitcraze (official docs)

* Getting started with the AI-Deck (setup + firmware baseline). ([Bitcraze][1])

```text
https://www.bitcraze.io/documentation/tutorials/getting-started-with-aideck/
```

* WiFi Video Streamer example (wifi-img-streamer overview). ([Bitcraze][2])

```text
https://www.bitcraze.io/documentation/repository/aideck-gap8-examples/master/examples/wifi-streamer/
```

* AI-deck GAP8 examples index (browse other camera + ML examples). ([Bitcraze][3])

```text
https://www.bitcraze.io/documentation/repository/aideck-gap8-examples/master/examples/
```

* Step-by-step guide to develop for GAP8 (useful when you start editing the streamer or building your own app). ([Bitcraze][3])

```text
https://www.bitcraze.io/documentation/repository/aideck-gap8-examples/master/guides/step-by-step-gap8-development/
```

* cflib Commander API docs (setpoint units; yaw rates are in degrees/s). ([Bitcraze][4])

```text
https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/api/cflib/crazyflie/commander/
```

* Crazyflie firmware “Commander framework” (how setpoints flow through the firmware). ([Bitcraze][5])

```text
https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/functional-areas/sensor-to-control/commanders_setpoints/
```

### GitHub (upstream repos)

* aideck-gap8-examples (source for wifi-img-streamer and other GAP8 examples). ([GitHub][6])

```text
https://github.com/bitcraze/aideck-gap8-examples
```

* crazyflie-lib-python (source for `cflib`, including `commander.py`). ([GitHub][7])

```text
https://github.com/bitcraze/crazyflie-lib-python
```

### Research papers

* E2EdgeAI: Energy-Efficient Edge Computing for Deployment of Vision-Based DNNs on Autonomous Tiny Drones (paper landing page). ([Semantic Scholar][8])

```text
https://www.semanticscholar.org/paper/E2EdgeAI%3A-Energy-Efficient-Edge-Computing-for-of-on-Navardi-Humes/2c7c3944fbfc51364a03bbe3edc7dd2b08c494f4
```

* AI and Vision based Autonomous Navigation of Nano-Drones in Partially-Known Environments (arXiv PDF).

```text
https://arxiv.org/pdf/2505.04972
```

[1]: https://www.bitcraze.io/documentation/tutorials/getting-started-with-aideck/?utm_source=chatgpt.com "Getting started with the AI deck"
[2]: https://www.bitcraze.io/documentation/repository/aideck-gap8-examples/master/examples/wifi-streamer/?utm_source=chatgpt.com "WiFi Video Streamer"
[3]: https://www.bitcraze.io/documentation/repository/aideck-gap8-examples/master/examples/?utm_source=chatgpt.com "Examples"
[4]: https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/api/cflib/crazyflie/commander/?utm_source=chatgpt.com "commander"
[5]: https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/functional-areas/sensor-to-control/commanders_setpoints/?utm_source=chatgpt.com "The Commander Framework"
[6]: https://github.com/bitcraze/AIdeck_examples/releases?utm_source=chatgpt.com "Releases · bitcraze/aideck-gap8-examples"
[7]: https://github.com/bitcraze/crazyflie-lib-python/blob/master/cflib/crazyflie/commander.py?utm_source=chatgpt.com "crazyflie-lib-python/cflib/crazyflie/commander.py at master"
[8]: https://www.semanticscholar.org/paper/E2EdgeAI%3A-Energy-Efficient-Edge-Computing-for-of-on-Navardi-Humes/2c7c3944fbfc51364a03bbe3edc7dd2b08c494f4?utm_source=chatgpt.com "E2EdgeAI: Energy-Efficient Edge Computing for Deployment of ..."

