Here's a clean and easy-to-follow `README.md` you can paste into your GitHub repo. It walks through **formation flight with two Crazyflie drones** using Python.

---

````markdown
Formation Flight with Two Crazyflie Drones
==========================================

This guide helps you set up and fly two Crazyflie 2.1 drones in formation using Python.

What You'll Need
----------------

- 2x Crazyflie 2.1 drones
- 1x Crazyradio PA USB dongle
- A Linux or macOS laptop
- Charged batteries in both drones
- Open indoor area to fly safely
- Python 3 installed on your machine

Step 1: Set Up Python Environment
---------------------------------

Create and activate a virtual environment:

```bash
python3 -m venv cf-env
source cf-env/bin/activate
````

Install the Crazyflie Python library:

```bash
pip install cflib
```

## Step 2: Power On the Drones

1. Connect the Crazyradio PA to your laptop.
2. Power on both drones by connecting their batteries.
3. Place them on a flat surface. Wait for the blinking LEDs to stabilize.

## Step 3: Create the Formation Flight Script

Create a file called `formation_flight.py`:

```bash
touch formation_flight.py
```

Then paste in the following code:

```python
import time, os
from cflib.crtp import init_drivers, scan_interfaces
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

init_drivers()
uris = [u for u, _ in scan_interfaces() if u.startswith("radio://")]
if len(uris) < 2:
    raise SystemExit(f"Need at least two Crazyflies (found {len(uris)})")
uris.sort(key=lambda u: ("2M" not in u, u))
uri1, uri2 = uris[0], uris[1]

hover = int(os.getenv("HOVER_THRUST", "50000"))
climb = int(os.getenv("CLIMB_THRUST", "57000"))
t_up = float(os.getenv("CLIMB_TIME", "0.6"))
dt = 0.02

def prepare(cf):
    for p, v in (("commander.enHighLevel", "0"), ("stabilizer.estimator", "1")):
        try:
            cf.param.set_value(p, v)
        except:
            pass

with SyncCrazyflie(uri1, cf=Crazyflie()) as scf1, SyncCrazyflie(uri2, cf=Crazyflie()) as scf2:
    cf1, cf2 = scf1.cf, scf2.cf
    prepare(cf1)
    prepare(cf2)
    cmds = [cf1.commander, cf2.commander]

    for _ in range(30):
        for cmd in cmds:
            cmd.send_setpoint(0, 0, 0, 0)
        time.sleep(dt)

    for i in range(1, 26):
        thrust = hover * i // 25
        for cmd in cmds:
            cmd.send_setpoint(0, 0, 0, thrust)
        time.sleep(dt)

    t0 = time.time()
    while time.time() - t0 < t_up:
        for cmd in cmds:
            cmd.send_setpoint(0, 0, 0, climb)
        time.sleep(dt)

    for i in range(25, -1, -1):
        thrust = hover * i // 25
        for cmd in cmds:
            cmd.send_setpoint(0, 0, 0, thrust)
        time.sleep(dt)

    for _ in range(25):
        for cmd in cmds:
            cmd.send_setpoint(0, 0, 0, 0)
        time.sleep(dt)
```

## Step 4: Run the Formation Flight

With both drones powered on and your virtual environment active, run:

```bash
python3 formation_flight.py
```

The drones will:

* Ramp up motors
* Take off and climb
* Hover briefly in sync
* Descend slowly
* Shut off their motors

## Tips

* Make sure both drones are using the same firmware version
* Ensure only two drones are powered on during flight
* If one drone isn't detected, use the `cfclient` to verify connectivity

```

---

Let me know if you want to include a troubleshooting section or a diagram of the formation!
```
