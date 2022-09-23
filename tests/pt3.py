import argparse
from collections import deque
import signal
from UDPComms import Publisher
import sys
import threading
import time


class PupTest(threading.Thread):
    """
    This class provides a user interface to send various UDP commands to
    the Mini Pupper

    To See Usage Type:
    python3 pt3.py --h

    The IP addresses are hard coded in UDPComms. The final version of the
    gateway will run on the robot where the IP address will be 127.0.0.1
    """

    def __init__(self, udp_port=8830,
                 file_name=None, wait_time=1000):
        """

        :param udp_port: Robot's UDP Port
        :param file_name: File containing UDP commands
        :param wait_time: time that wait command will wait in milliseconds
        """

        MESSAGE_RATE = 20
        self.min_msg = 5
        self.send_count = 0
        # UDP Action Packets
        self.deactivate = {
            "ly": 0,
            "lx": 0,
            "rx": 0,
            "ry": 0,
            "L2": 0,
            "R2": 0,
            "R1": 0,
            "L1": 0,
            "dpady": 0,
            "dpadx": 0,
            "x": 0,
            "square": 0,
            "circle": 0,
            "triangle": 0,
            "message_rate": MESSAGE_RATE,
        }

        self.activate = self.deactivate.copy()
        self.activate['L1'] = 1

        self.rest = self.deactivate.copy()

        self.trot = self.deactivate.copy()
        self.trot['R1'] = True

        self.raise_body = self.deactivate.copy()
        self.raise_body['dpady'] = 1

        self.lower_body = self.deactivate.copy()
        self.lower_body['dpady'] = -1

        self.roll_body_left = self.deactivate.copy()
        self.roll_body_left['dpadx'] = -1

        self.roll_body_right = self.deactivate.copy()
        self.roll_body_right['dpadx'] = 1

        self.move_forward_fast = self.deactivate.copy()
        self.move_forward_fast['ly'] = 1

        self.move_forward_slow = self.deactivate.copy()
        self.move_forward_slow['ly'] = 0.5

        self.move_back_fast = self.deactivate.copy()
        self.move_back_fast['ly'] = -1

        self.move_back_slow = self.deactivate.copy()
        self.move_back_slow['ly'] = -0.5

        self.move_left_fast = self.deactivate.copy()
        self.move_left_fast['lx'] = -1

        self.move_left_slow = self.deactivate.copy()
        self.move_left_slow['lx'] = -0.5

        self.move_right_fast = self.deactivate.copy()
        self.move_right_fast['lx'] = 1

        self.move_right_slow = self.deactivate.copy()
        self.move_right_slow['lx'] = 0.5

        self.yaw_left_mid = self.deactivate.copy()
        self.yaw_left_mid['rx'] =  -0.5

        self.yaw_left_max = self.deactivate.copy()
        self.yaw_left_max['rx'] =  -1.0

        self.yaw_right_mid = self.deactivate.copy()
        self.yaw_right_mid['rx'] =  0.5

        self.yaw_right_max = self.deactivate.copy()
        self.yaw_right_max['rx'] =  1.0

        self.pitch_down_mid = self.deactivate.copy()
        self.pitch_down_mid['ry'] =  0.5

        self.pitch_down_max = self.deactivate.copy()
        self.pitch_down_max['ry'] =  1.0

        self.pitch_up_mid = self.deactivate.copy()
        self.pitch_up_mid['ry'] =  -0.5

        self.pitch_up_max = self.deactivate.copy()
        self.pitch_up_max['ry'] =  -1.0

        self.shutdown = self.deactivate.copy()
        self.shutdown['triangle'] = True

        # initialize threading parent
        threading.Thread.__init__(self)

        # create a thread to get next activity
        self.command_input_thread = threading.Thread(target=self._get_next_command)
        self.command_input_thread.daemon = True

        # flag to allow the reporter and receive threads to run.
        self.run_event = threading.Event()

        # create a deque to buffer incoming activity commands
        self.the_deque = deque()

        self.udp_port = udp_port

        self.file_name = file_name
        self.wait_time = wait_time

        # create a UDP client
        self.pub = Publisher(8830, 65520)
        print("Mini Pupper Exerciser version 1.0")
        print()
        print(f'Port = {self.udp_port}')

        # a dictionary of commands and handler functions
        self.exec_commands = {0: self.list_commands, 1: self.activate_robot,
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
                              22: self.do_move_right_slow, 23: self.deactivate_robot,
                              24: self.shutdown_robot, 25: self.kill_time,
                              26: self.set_rest_mode,
                              98: self.clear,
                              99: self.out_of_here,
                              }

        self.the_command = 23
        self.command_input_thread.start()
        self._run_threads()

        while True:
            try:
                if len(self.the_deque) and self.send_count > self.min_msg:
                    self.the_command = self.the_deque.popleft()
                    self.send_count = 0
                    if self.the_command == 98:
                        self.the_command = None

                if self.the_command:
                    self.exec_commands[self.the_command]()
                    self.send_count += 1

                # Message rate expected by minipupper
                time.sleep(1 / MESSAGE_RATE)

            except KeyboardInterrupt:
                self._stop_threads()
                time.sleep(1)
                sys.exit(0)

    @staticmethod
    def list_commands():
        print('0=List Commands\t\t1=Activate Robot\t2=Set Trot Mode\n')
        print("3=Raise Body\t\t4=Lower Body\t\t5=Roll Body Left\t6=Roll Body Right")
        print("7=Yaw Left Mid\t\t8=Yaw Left Max\t\t9=Yaw Right Mid\t\t10=Yaw Right Max")
        print(
            "11=Pitch Down Mid\t12=Pitch Down Max\t13=Pitch Up Mid\t\t14=Pitch Up Max\n")
        print("15=Forward Fast\t\t16=Forward Slow\t\t17=Reverse Fast\t\t18=Reverse "
              "Slow")
        print("19=Left Fast\t\t20=Left Slow\t\t21=Right Fast\t\t22=Right Slow")
        print("23=Deactivate\t\t24=Shutdown\t\t26=Set Rest Mode")

    def activate_robot(self):
        self.pub.send(self.activate)

    def set_rest_mode(self):
        self.pub.send(self.rest)

    def set_trot_mode(self):
        self.pub.send(self.trot)

    def deactivate_robot(self):
        self.pub.send(self.deactivate)

    def raise_the_body(self):
        self.pub.send(self.raise_body)

    def lower_the_body(self):
        self.pub.send(self.lower_body)

    def roll_the_body_left(self):
        self.pub.send(self.roll_body_left)

    def roll_the_body_right(self):
        self.pub.send(self.roll_body_right)

    def do_yaw_left_mid(self):
        self.pub.send(self.yaw_left_mid)

    def do_yaw_left_max(self):
        self.pub.send(self.yaw_left_max)

    def do_yaw_right_mid(self):
        self.pub.send(self.yaw_right_mid)

    def do_yaw_right_max(self):
        self.pub.send(self.yaw_right_max)

    def do_pitch_down_mid(self):
        self.pub.send(self.pitch_down_mid)

    def do_pitch_down_max(self):
        self.pub.send(self.pitch_down_max)

    def do_pitch_up_mid(self):
        self.pub.send(self.pitch_up_mid)

    def do_pitch_up_max(self):
        self.pub.send(self.pitch_up_max)

    def do_move_left_slow(self):
        self.pub.send(self.move_left_slow)

    def do_move_left_fast(self):
        self.pub.send(self.move_left_fast)

    def do_move_right_slow(self):
        self.pub.send(self.move_right_slow)

    def do_move_right_fast(self):
        self.pub.send(self.move_right_fast)

    def do_move_forward_slow(self):
        self.pub.send(self.move_forward_slow)

    def do_move_forward_fast(self):
        self.pub.send(self.move_forward_fast)

    def do_move_back_slow(self):
        self.pub.send(self.move_back_slow)

    def do_move_back_fast(self):
        self.pub.send(self.move_back_fast)

    def kill_time(self):
        time.sleep(self.wait_time)

    def shutdown_robot(self):
        self.pub.send(self.shutdown)

    def clear(self):
        pass

    def out_of_here(self):
        self._stop_threads()
        sys.exit(0)

    def _run_threads(self):
        self.run_event.set()

    def _is_running(self):
        return self.run_event.is_set()

    def _stop_threads(self):
        self.run_event.clear()

    def _get_next_command(self):
        self.run_event.wait()

        while self._is_running():
            # print("\nCOMMANDS: ")
            # self.list_commands()
            command = None

            # if file was specified, get commands from the file
            try:
                command_list = []
                echo_list = []
                echo_cmd = 1000
                # wait until a few default messages are sent
                time.sleep(.2)
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
                    command_list.append(99)
                    print(f'Commands Read From File: {command_list}')
                for command in command_list:

                    # activate and toggle mode do not need to be run in a loop
                    if command == 25:
                        #print(f'Processing Command: {command}')
                        time.sleep(self.wait_time / 1000)
                        #print(f"Killing time for {self.wait_time/1000} seconds")
                        continue
                    elif command == 99:
                        print("Exiting\n\n")
                    elif command >= 1000:
                        print(f'>>>>>>>>> {echo_list[command-1000]}')
                        continue
                    self.the_deque.append(command)

            except KeyboardInterrupt:
                raise KeyboardInterrupt


def pt():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", dest="udp_port", default="8830",
                        help="Mini Pupper UDP Port Number")

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
    kw_options = {'udp_port': int(args.udp_port),
                  'file_name': fn,
                  'wait_time': int(args.wait_time)
                  }

    PupTest(**kw_options)
    sys.exit(0)


# signal handler function called when Control-C occurs
def signal_handler(sig, frame):
    print('Exiting Through Signal Handler')
    raise KeyboardInterrupt


# listen for SIGINT
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    pt()
