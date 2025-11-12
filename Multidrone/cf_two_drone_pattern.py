cat > ~/crazyflie/cf_two_drone_pattern.py <<'PY'
import time
from cflib.crtp import init_drivers, scan_interfaces
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

init_drivers()

uris = [uri for uri, _ in scan_interfaces() if uri.startswith("radio://")]
if len(uris) < 2:
    raise SystemExit("Need at least two Crazyflies (found {})".format(len(uris)))

uri1, uri2 = uris[0], uris[1]
print(f"Using drones: {uri1} and {uri2}")

def fly_pattern(mc1, mc2):
    mc1.take_off(0.5, 2.0)
    mc2.take_off(0.5, 2.0)
    time.sleep(2)

    side = 0.5  # meters
    delay = 1.0

    mc1.forward(side)
    mc2.back(side)
    time.sleep(delay)

    mc1.right(side)
    mc2.left(side)
    time.sleep(delay)

    mc1.back(side)
    mc2.forward(side)
    time.sleep(delay)

    mc1.left(side)
    mc2.right(side)
    time.sleep(delay)

    mc1.stop()
    mc2.stop()
    time.sleep(0.5)

    mc1.land(0.2, 2.0)
    mc2.land(0.2, 2.0)

with SyncCrazyflie(uri1, cf=Crazyflie()) as scf1, SyncCrazyflie(uri2, cf=Crazyflie()) as scf2:
    scf1.cf.param.set_value('commander.enHighLevel', '1')
    scf2.cf.param.set_value('commander.enHighLevel', '1')

    with MotionCommander(scf1, default_height=0.5) as mc1, MotionCommander(scf2, default_height=0.5) as mc2:
        fly_pattern(mc1, mc2)
PY
