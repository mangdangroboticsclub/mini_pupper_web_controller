import filecmp
import os
import time
from joystick_sim.joystick import Joystick

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
    assert filecmp.cmp(os.path.join(os.path.dirname(__file__), 'expected_results', 'seq_log_1'),
                       '/tmp/log.txt')

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
    assert filecmp.cmp(os.path.join(os.path.dirname(__file__), 'expected_results', 'seq_log_2'),
                       '/tmp/log.txt')

if __name__ == "__main__":
    test_trot()
