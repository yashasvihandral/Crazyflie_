
Getting Started with Multi-Drone Crazyflie Flight

This tutorial shows you how to:


- **Set up your system to fly two Crazyflie drones**
- **Install the necessary software**
- **Connect to both drones using Crazyradio PA**
- **Run a Python script that lifts both drones in sync and lands them smoothly**



**What You Need**

- Two Crazyflie 2.1 nano quadcopters  
- Two Crazyradio PA USB dongles  
- Fully charged batteries in both drones  
- A macOS or Linux laptop  
- A large, open, and safe indoor space to fly two drones



**Step 1: Install Python 3**

On macOS:

```bash
brew install python
````

On Ubuntu:

```bash
sudo apt update
sudo apt install python3 python3-pip
```

**Verify that Python is installed:**

```bash
python3 --version
pip3 --version
```



**Step 2: Set Up a Virtual Environment and Install Libraries**

**Create and activate a virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Install the Crazyflie Python library:**

```bash
pip install cflib
```



**Step 3: Create the Multi-Drone Flight Script**

**Use this command to generate the script from your terminal:**

```bash
cat > ~/crazyflie/cf_up_min.py <<'PY'
import time, os
from cflib.crtp import init_drivers, scan_interfaces
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

init_drivers()
uris = [u for u, _ in scan_interfaces() if u.startswith("radio://")]
if len(uris) < 2: raise SystemExit("Need at least two Crazyflies (found {})".format(len(uris)))
uris.sort(key=lambda u: ("2M" not in u, u))  # prefer 2M
uri1, uri2 = uris[0], uris[1]

hover = int(os.getenv("HOVER_THRUST", "50000"))
climb = int(os.getenv("CLIMB_THRUST", "57000"))
t_up = float(os.getenv("CLIMB_TIME", "0.6"))
dt = 0.02

def prepare(cf):
    for p, v in (("commander.enHighLevel", "0"), ("stabilizer.estimator", "1")):
        try: cf.param.set_value(p, v)
        except: pass

with SyncCrazyflie(uri1, cf=Crazyflie()) as scf1, SyncCrazyflie(uri2, cf=Crazyflie()) as scf2:
    cf1, cf2 = scf1.cf, scf2.cf
    prepare(cf1)
    prepare(cf2)
    cmds = [cf1.commander, cf2.commander]

    for _ in range(30):
        for cmd in cmds: cmd.send_setpoint(0,0,0,0)
        time.sleep(dt)

    for i in range(1, 26):
        thrust = hover * i // 25
        for cmd in cmds: cmd.send_setpoint(0,0,0,thrust)
        time.sleep(dt)

    t0 = time.time()
    while time.time() - t0 < t_up:
        for cmd in cmds: cmd.send_setpoint(0,0,0,climb)
        time.sleep(dt)

    for i in range(25, -1, -1):
        thrust = hover * i // 25
        for cmd in cmds: cmd.send_setpoint(0,0,0,thrust)
        time.sleep(dt)

    for _ in range(25):
        for cmd in cmds: cmd.send_setpoint(0,0,0,0)
        time.sleep(dt)
PY
```

This command writes the full script to `~/crazyflie/cf_up_min.py`.



**Step 4: Power On and Connect the Drones**

1. **Plug both Crazyradio PA USB dongles** into your computer
2. **Connect fully charged batteries** to both Crazyflie drones
3. **Wait for LEDs to finish blinking**, indicating they are ready
4. **Place both drones flat** on a level surface


**Step 5: Run the Flight Script**

Make sure your virtual environment is active and run the script:

```bash
cd ~/crazyflie
source ../venv/bin/activate
python3 cf_up_min.py
```



**What the Drones Will Do**

* **Initialize and stabilize**
* **Ramp up motor thrust gradually**
* **Climb together**
* **Hover briefly**
* **Descend smoothly**
* **Stop motors completely after landing**



