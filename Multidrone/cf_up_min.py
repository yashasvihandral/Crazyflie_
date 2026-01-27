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
