import os
import time
from joystick_sim.joystick import Joystick, Check


def test_cancel_shutdown():
    os.system("rm -f /tmp/log.txt")
    joystick = Joystick()
    joystick.write_log = True
    joystick.publish = False
    joystick.start()
    joystick.activate()
    time.sleep(0.5)
    joystick.push_triangle()
    joystick.push_L1()
    time.sleep(0.5)
    joystick.stop()
    joystick.join()
    check = Check('/tmp', os.path.join(os.path.dirname(__file__), 'expected_results'))
    assert check.compare_results('log.txt', 'seq_log_1')


def test_robot_activate_deactivate():
    os.system("rm -f /tmp/log.txt")
    joystick = Joystick()
    joystick.write_log = True
    joystick.publish = False
    joystick.start()
    joystick.activate()
    joystick.push_L1()
    time.sleep(1)
    joystick.push_L1()
    time.sleep(1)
    joystick.deactivate()
    joystick.stop()
    joystick.join()
    check = Check('/tmp', os.path.join(os.path.dirname(__file__), 'expected_results'))
    assert check.compare_results('log.txt', 'seq_log_2')


if __name__ == "__main__":
    test_robot_activate_deactivate()
