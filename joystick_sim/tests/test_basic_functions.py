import filecmp
import os
import time
from joystick_sim.joystick import Joystick

def test_activate_deactivate():
    os.system("rm -f /tmp/log.txt")
    joystick = Joystick()
    joystick.write_log = True
    joystick.publish = False
    joystick.start()
    joystick.activate()
    time.sleep(0.5)
    joystick.deactivate()
    time.sleep(0.5)
    joystick.stop()
    joystick.join()
    assert filecmp.cmp(os.path.join(os.path.dirname(__file__), 'expected_results', 'log_1'),
                       '/tmp/log.txt')

def test_push_L1():
    os.system("rm -f /tmp/log.txt")
    joystick = Joystick()
    joystick.write_log = True
    joystick.publish = False
    joystick.start()
    joystick.activate()
    joystick. push_L1()
    time.sleep(0.5)
    joystick.deactivate()
    time.sleep(0.5)
    joystick.stop()
    joystick.join()
    assert filecmp.cmp(os.path.join(os.path.dirname(__file__), 'expected_results', 'log_2'),
                       '/tmp/log.txt')

def test_push_R1():
    os.system("rm -f /tmp/log.txt")
    joystick = Joystick()
    joystick.write_log = True
    joystick.publish = False
    joystick.start()
    joystick.activate()
    joystick. push_R1()
    time.sleep(0.5)
    joystick.deactivate()
    time.sleep(0.5)
    joystick.stop()
    joystick.join()
    assert filecmp.cmp(os.path.join(os.path.dirname(__file__), 'expected_results', 'log_3'),
                       '/tmp/log.txt')

def test_push_x():
    os.system("rm -f /tmp/log.txt")
    joystick = Joystick()
    joystick.write_log = True
    joystick.publish = False
    joystick.start()
    joystick.activate()
    joystick. push_x()
    time.sleep(0.5)
    joystick.deactivate()
    time.sleep(0.5)
    joystick.stop()
    joystick.join()
    assert filecmp.cmp(os.path.join(os.path.dirname(__file__), 'expected_results', 'log_4'),
                       '/tmp/log.txt')

def test_push_circle():
    os.system("rm -f /tmp/log.txt")
    joystick = Joystick()
    joystick.write_log = True
    joystick.publish = False
    joystick.start()
    joystick.activate()
    joystick. push_circle()
    time.sleep(0.5)
    joystick.deactivate()
    time.sleep(0.5)
    joystick.stop()
    joystick.join()
    assert filecmp.cmp(os.path.join(os.path.dirname(__file__), 'expected_results', 'log_5'),
                       '/tmp/log.txt')

def test_push_triangle():
    os.system("rm -f /tmp/log.txt")
    joystick = Joystick()
    joystick.write_log = True
    joystick.publish = False
    joystick.start()
    joystick.activate()
    joystick.push_triangle()
    time.sleep(0.5)
    joystick.deactivate()
    time.sleep(0.5)
    joystick.stop()
    joystick.join()
    with open('/tmp/log.txt') as fh:
        results = fh.readlines()
    with open(os.path.join(os.path.dirname(__file__), 'expected_results', 'log_6')) as fh:
        expected = fh.readlines()
    comp_len = min(len(results), len(expected))
    # triangle is mapped to shutdown in the Stanford code
    # the simulator simulates the triangle key being pressed continuously
    # the lenght of the log file varies, we test that the beginning matches (and that there is output)
    assert comp_len > 20
    assert results[0:comp_len] == expected[0:comp_len]

def test_set_velocity():
    os.system("rm -f /tmp/log.txt")
    joystick = Joystick()
    joystick.write_log = True
    joystick.publish = False
    joystick.start()
    joystick.activate()
    joystick.set_velocity(.5, .5)
    time.sleep(0.5)
    joystick.deactivate()
    time.sleep(0.5)
    joystick.stop()
    joystick.join()
    assert filecmp.cmp(os.path.join(os.path.dirname(__file__), 'expected_results', 'log_7'),
                       '/tmp/log.txt')

def test_set_yaw():
    os.system("rm -f /tmp/log.txt")
    joystick = Joystick()
    joystick.write_log = True
    joystick.publish = False
    joystick.start()
    joystick.activate()
    joystick.set_yaw(.5)
    time.sleep(0.5)
    joystick.deactivate()
    time.sleep(0.5)
    joystick.stop()
    joystick.join()
    assert filecmp.cmp(os.path.join(os.path.dirname(__file__), 'expected_results', 'log_8'),
                       '/tmp/log.txt')

def test_set_pitch():
    os.system("rm -f /tmp/log.txt")
    joystick = Joystick()
    joystick.write_log = True
    joystick.publish = False
    joystick.start()
    joystick.activate()
    joystick.set_pitch(.5)
    time.sleep(0.5)
    joystick.deactivate()
    time.sleep(0.5)
    joystick.stop()
    joystick.join()
    assert filecmp.cmp(os.path.join(os.path.dirname(__file__), 'expected_results', 'log_9'),
                       '/tmp/log.txt')

def test_adjust_roll():
    os.system("rm -f /tmp/log.txt")
    joystick = Joystick()
    joystick.write_log = True
    joystick.publish = False
    joystick.start()
    joystick.activate()
    joystick.adjust_roll(-1)
    time.sleep(0.5)
    joystick.deactivate()
    time.sleep(0.5)
    joystick.stop()
    joystick.join()
    assert filecmp.cmp(os.path.join(os.path.dirname(__file__), 'expected_results', 'log_10'),
                       '/tmp/log.txt')

def test_adjust_height():
    os.system("rm -f /tmp/log.txt")
    joystick = Joystick()
    joystick.write_log = True
    joystick.publish = False
    joystick.start()
    joystick.activate()
    joystick.adjust_height(-1)
    time.sleep(0.5)
    joystick.deactivate()
    time.sleep(0.5)
    joystick.stop()
    joystick.join()
    assert filecmp.cmp(os.path.join(os.path.dirname(__file__), 'expected_results', 'log_11'),
                       '/tmp/log.txt')

if __name__ == "__main__":
    test_push_triangle()
