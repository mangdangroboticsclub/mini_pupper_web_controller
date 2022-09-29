import os
import time
from joystick_sim.joystick import Joystick


def compare_files_truncated(expected, result):
    with open(result, 'r') as fh:
        res = fh.readlines()
    with open(expected, 'r') as fh:
        exp = fh.readlines()
    cmp_len = min(len(res), len(exp))
    if cmp_len < len(exp):
        # improve expected
        return False
    return res[0:cmp_len] == exp[0:cmp_len]


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
    assert compare_files_truncated(os.path.join(os.path.dirname(__file__), 'expected_results', 'seq_log_1'),
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
    assert compare_files_truncated(os.path.join(os.path.dirname(__file__), 'expected_results', 'seq_log_2'),
                                   '/tmp/log.txt')


if __name__ == "__main__":
    test_robot_activate_deactivate()
