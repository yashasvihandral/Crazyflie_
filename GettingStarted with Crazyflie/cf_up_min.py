cat > ~/crazyflie/cf_up_min.py <<'PY'
import time, os, math
from cflib.crtp import init_drivers, scan_interfaces
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

init_drivers()
uris = [u for u, _ in scan_interfaces() if u.startswith("radio://")]
if not uris: raise SystemExit("No Crazyflie found")
uris.sort(key=lambda u: ("2M" not in u, u))
uri = uris[0]

hover = int(os.getenv("HOVER_THRUST", "50000"))
climb = int(os.getenv("CLIMB_THRUST", "57000"))
t_up = float(os.getenv("CLIMB_TIME", "0.6"))
dt = 0.015  # finer resolution

with SyncCrazyflie(uri, cf=Crazyflie()) as scf:
    cf = scf.cf
    for p, v in (("commander.enHighLevel", "0"), ("stabilizer.estimator", "1")):
        try:
            cf.param.set_value(p, v)
        except Exception:
            pass

    cmd = cf.commander

    # Arm motors gently
    for _ in range(30):
        cmd.send_setpoint(0, 0, 0, 0)
        time.sleep(dt)

    # Smooth takeoff ramp
    for i in range(1, 26):
        cmd.send_setpoint(0, 0, 0, hover * i // 25)
        time.sleep(dt)

    # Climb to hover
    t0 = time.time()
    while time.time() - t0 < t_up:
        cmd.send_setpoint(0, 0, 0, climb)
        time.sleep(dt)

    # --- COSINE EASED LANDING ---
    descent_steps = 80
    for i in range(descent_steps + 1):
        ratio = 0.5 * (1 + math.cos(math.pi * i / descent_steps))  # cosine ease-out
        thrust = int(hover * ratio)
        cmd.send_setpoint(0, 0, 0, thrust)
        time.sleep(dt)

    # Cushion thrust (optional: prevent motor cutout too fast)
    for _ in range(10):
        cmd.send_setpoint(0, 0, 0, 18000)
        time.sleep(dt)

    # Fully stop motors
    for _ in range(20):
        cmd.send_setpoint(0, 0, 0, 0)
        time.sleep(dt)
PY

python3 ~/crazyflie/cf_up_min.py
