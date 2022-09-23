import argparse
import time
import sys
from joystick_sim.joystick import Joystick


class PupTest():
    """
    This class provides a user interface to send various UDP commands to
    the Mini Pupper

    To See Usage Type:
    python3 pt3.py --h

    The IP addresses are hard coded in UDPComms. The final version of the
    gateway will run on the robot where the IP address will be 127.0.0.1
    """

    def __init__(self,
                 file_name=None, wait_time=1000):
        """

        :param file_name: File containing UDP commands
        :param wait_time: time that wait command will wait in milliseconds
        """

        self.file_name = file_name
        self.wait_time = wait_time/1000

        self.joystick = Joystick()
        self.joystick.start()
        self.joystick.activate()
        time.sleep(0.5)

        print("Mini Pupper Exerciser version 1.0")
        print()

        # a dictionary of commands and handler functions
        self.exec_commands = {1: self.activate_robot,
                              2: self.set_trot_mode, 3: self.raise_the_body,
                              4: self.lower_the_body, 5: self.roll_the_body_left,
                              6: self.roll_the_body_right, 7: self.do_yaw_left_mid,
                              8: self.do_yaw_left_max, 9: self.do_yaw_right_mid,
                              10: self.do_yaw_right_max, 11: self.do_pitch_down_mid,
                              12: self.do_pitch_down_max, 13: self.do_pitch_up_mid,
                              14: self.do_pitch_up_max, 15: self.do_move_forward_fast,
                              16: self.do_move_forward_slow, 17: self.do_move_back_fast,
                              18: self.do_move_back_slow, 19: self.do_move_left_fast,
                              20: self.do_move_left_slow, 21: self.do_move_right_fast,
                              22: self.do_move_right_slow,
                              24: self.shutdown_robot, 25: self.kill_time,
                              26: self.jump, 27: self.do_pitch_neutral, 
                              28: self.do_yaw_neutral,
                              }

        command_list = []
        echo_list = []
        echo_cmd = 1000

        with open(self.file_name, encoding="utf-8") as f:
            while (line := f.readline()):
                if not len(line.strip()):
                    continue
                if line.lstrip()[0:4] == 'echo':
                    command_list.append(echo_cmd)
                    echo_list.append(line.lstrip()[5:])
                    echo_cmd += 1
                    continue
                if line.lstrip()[0] == '#':
                    continue
                command_list.append(int(line.lstrip().replace('=', ' ').split(' ')[0]))
            print(f'Commands Read From File: {command_list}')
        for command in command_list:

            if command >= 1000:
                print(f'>>>>>>>>> {echo_list[command-1000]}')
                continue
            self.exec_commands[command]()

        self.joystick.stop()

    def activate_robot(self):
        self.joystick.push_L1()

    def jump(self):
        self.joystick.push_x()

    def set_trot_mode(self):
        self.joystick.push_R1()

    def raise_the_body(self):
        self.joystick.adjust_height(1)

    def lower_the_body(self):
        self.joystick.adjust_height(-1)

    def roll_the_body_left(self):
        self.joystick.adjust_roll(-1)

    def roll_the_body_right(self):
        self.joystick.adjust_roll(1)

    def do_yaw_left_mid(self):
        self.joystick.set_yaw(-0.5)

    def do_yaw_left_max(self):
        self.joystick.set_yaw(-1.0)

    def do_yaw_right_mid(self):
        self.joystick.set_yaw(0.5)

    def do_yaw_right_max(self):
        self.joystick.set_yaw(1.0)

    def do_yaw_neutral(self):
        self.joystick.set_yaw(0.0)

    def do_pitch_down_mid(self):
        self.joystick.set_pitch(0.5)

    def do_pitch_down_max(self):
        self.joystick.set_pitch(1.0)

    def do_pitch_up_mid(self):
        self.joystick.set_pitch(-0.5)

    def do_pitch_up_max(self):
        self.joystick.set_pitch(-1.0)

    def do_pitch_neutral(self):
        self.joystick.set_pitch(0.0)

    def do_move_left_slow(self):
        self.joystick.set_velocity(0.0, -0.5)

    def do_move_left_fast(self):
        self.joystick.set_velocity(0.0, -1.0)

    def do_move_right_slow(self):
        self.joystick.set_velocity(0.0, 0.5)

    def do_move_right_fast(self):
        self.joystick.set_velocity(0.0, 1.0)

    def do_move_forward_slow(self):
        self.joystick.set_velocity(0.5, 0.0)

    def do_move_forward_fast(self):
        self.joystick.set_velocity(1.0, 0.0)

    def do_move_back_slow(self):
        self.joystick.set_velocity(-0.5, 0.0)

    def do_move_back_fast(self):
        self.joystick.set_velocity(-1.0, 0.0)

    def kill_time(self):
        time.sleep(self.wait_time)

    def shutdown_robot(self):
        self.joystick.push_triange()


def pt():
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", dest="file_name", default="None",
                        help="Command File containing commands")

    parser.add_argument("-w", dest="wait_time", default="1000",
                        help="Wait command wait time in milliseconds")

    args = parser.parse_args()

    if args.file_name == "None":
        print("missing parameter file_name")
        sys.exit(1)
    else:
        fn = args.file_name
    kw_options = {'file_name': fn,
                  'wait_time': int(args.wait_time)
                  }

    PupTest(**kw_options)
    sys.exit(0)


if __name__ == '__main__':
    pt()
